import pandas
from colorama import Fore, Style
from prettytable import PrettyTable
from Sources.Excel.Configuration.Config import Config
from Sources.Excel.Reader.Row import Row


def read(excel_file_path: str, parsing_config: Config.Parsing) -> dict[str, list[Row]]:
    excel_file = pandas.ExcelFile(excel_file_path)
    rows_by_sheet_name = {}

    for sheet_name in parsing_config.ordered_by_level_sheet_names:
        excel_sheet_data_frame = excel_file.parse(sheet_name, header=None, index_col=None)
        rows_by_sheet_name[sheet_name] = _ReadRows(sheet_name, excel_sheet_data_frame, parsing_config)

    return rows_by_sheet_name


def _ReadRows(sheet_name: str, excel_sheet_data_frame: pandas.DataFrame, parsing_config: Config.Parsing) -> \
        list[Row]:
    result = []

    index: int
    for index, excel_row in excel_sheet_data_frame.iterrows():
        if index < parsing_config.start_parsing_row_index:
            continue

        if not _NeedIgnoreRow(sheet_name, index, excel_row, parsing_config.ignore_column_index):
            link_id = _ReadCellValue(excel_row.iloc[parsing_config.link_id_column_index])
            field_name = _ReadCellValue(excel_row.iloc[parsing_config.field_name_column_index])
            field_value_type = _ReadCellValue(excel_row.iloc[parsing_config.field_value_type_column_index])
            field_value = _ReadCellValue(excel_row.iloc[parsing_config.field_value_column_index])
            alias_func_arg_value = _ReadCellValue(excel_row.iloc[parsing_config.alias_func_arg_value_column_index])

            is_empty_row = (
                    link_id is None
                    and field_name is None
                    and field_value_type is None
                    and field_value is None
                    and alias_func_arg_value is None)

            if not is_empty_row:
                result.append(Row(index, link_id, field_name, field_value_type, field_value, alias_func_arg_value))

    return result


def _ReadCellValue(cell):
    return str(cell).strip() if not _IsEmptyCell(cell) else None


def _NeedIgnoreRow(sheet_name: str, row_index: int, excel_row, ignore_column_index: int):
    ignore_cell = excel_row.iloc[ignore_column_index]

    if _IsEmptyCell(ignore_cell):
        return False

    ignore_value = str(ignore_cell).lower()
    if ignore_value == 'true' or ignore_value == '1':
        return True
    if ignore_value == 'false' or ignore_value == '0':
        return False

    print(f"{Fore.YELLOW}Warning:  ignore type should be bool.{Style.RESET_ALL}")

    table = PrettyTable()
    table.field_names = ["Sheet name", "Row index", "ignore", ]
    highlighted_ignore_value = "".join([Fore.YELLOW, ignore_value, Style.RESET_ALL])
    table.add_row([sheet_name, row_index, highlighted_ignore_value])

    print(f"{str(table)}\n")
    return False


def _IsEmptyCell(ignore_value):
    return pandas.isna(ignore_value) or pandas.isnull(ignore_value)
