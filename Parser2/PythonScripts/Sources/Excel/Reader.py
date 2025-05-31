import pandas
from typing import Optional
from prettytable import PrettyTable
from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.Row import Row
from Tests import LogFormatter


def read(excel_file_path: str, parsing_config: ParsingConfig) -> dict[str, list[Row]]:
    excel_file = pandas.ExcelFile(excel_file_path)
    rows_by_sheet_name = {}

    for sheet_name in parsing_config.ordered_by_level_sheet_names:
        if sheet_name in excel_file.sheet_names:
            excel_sheet_data_frame = excel_file.parse(sheet_name, index_col=None)
            rows_by_sheet_name[sheet_name] = _ReadRows(sheet_name, excel_sheet_data_frame, parsing_config)
        else:
            print(LogFormatter.formatErrorColor(f"Error: sheet name '{sheet_name}' not found."))

    return rows_by_sheet_name


def _ReadRows(sheet_name: str, excel_sheet_data_frame: pandas.DataFrame, parsing_config: ParsingConfig) -> list[Row]:
    result = []

    index: int
    for index, excel_row in excel_sheet_data_frame.iterrows():
        if index < parsing_config.start_parsing_row_index:
            continue

        if not _NeedIgnoreRow(sheet_name, index, excel_row, parsing_config.ignore_column_name):
            link_id = _ReadCellValue(excel_row, parsing_config.link_id_column_name)
            field_name = _ReadCellValue(excel_row, parsing_config.field_name_column_name)
            field_value_type = _ReadCellValue(excel_row, parsing_config.field_value_type_column_name)
            field_value = _ReadCellValue(excel_row, parsing_config.field_value_column_name)
            alias_func_arg_value = _ReadCellValue(excel_row, parsing_config.alias_func_arg_value_column_name)

            is_empty_row = (
                    link_id is None
                    and field_name is None
                    and field_value_type is None
                    and field_value is None
                    and alias_func_arg_value is None)

            if not is_empty_row:
                anonym_args: Optional[dict[str, str]] = \
                    __ReadAnonymArgs(excel_row, parsing_config.anonym_alias_func_arg_name_by_column_name)
                visible_number = _ConvertIndexToVisibleNumber(index)
                row = Row(visible_number, link_id, field_name, field_value_type, field_value, alias_func_arg_value,
                          anonym_args)
                result.append(row)

    return result


def __ReadAnonymArgs(excel_row, anonym_alias_func_arg_name_by_column_name: dict[str, str]) -> Optional[dict[str, str]]:
    result: Optional[dict[str, str]] = None

    for column_name, arg_name in anonym_alias_func_arg_name_by_column_name.items():
        cell_value = _ReadCellValue(excel_row, column_name)
        if cell_value is not None:
            if result is None:
                result = {}
            result[arg_name] = cell_value

    return result


def _NeedIgnoreRow(sheet_name: str, row_index: int, excel_row, ignore_column_name: str):
    ignore_value = _ReadCellValue(excel_row, ignore_column_name)

    if ignore_value is None:
        return False

    ignore_value = str(ignore_value).lower()
    if ignore_value == 'true' or ignore_value == '1' or ignore_value == '1.0':
        return True
    if ignore_value == 'false' or ignore_value == '0' or ignore_value == '0.0':
        return False

    print(LogFormatter.formatWarningColor('Warning: ignore type should be bool.'))

    table = PrettyTable()
    table.field_names = ["Sheet name", "Row index", "ignore", ]
    highlighted_ignore_value = LogFormatter.formatWarningColor(ignore_value)
    table.add_row([sheet_name, row_index, highlighted_ignore_value])

    print(f"{str(table)}\n")
    return False


def _ReadCellValue(excel_row, column_name: str) -> Optional[str]:
    if column_name not in excel_row:
        return None

    cell = excel_row.at[column_name]
    return str(cell).strip() if not _IsEmptyCell(cell) else None


def _IsEmptyCell(ignore_value):
    return pandas.isna(ignore_value) or pandas.isnull(ignore_value)


def _ConvertIndexToVisibleNumber(index: int) -> int:
    hidden_title = 1
    title = 1

    return index + hidden_title + title
