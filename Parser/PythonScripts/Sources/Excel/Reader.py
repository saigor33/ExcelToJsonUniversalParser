import pandas
from typing import Optional
from prettytable import PrettyTable
from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.Row import Row
from Tests import LogFormatter


def read(excel_file_path: str, parsing_config: ParsingConfig) -> dict[str, list[Row]]:
    excel_file = pandas.ExcelFile(excel_file_path)
    rows_by_sheet_name = {}

    missing_sheet_names: Optional[list[str]] = None

    for sheet_name in parsing_config.ordered_by_level_sheet_names:
        if sheet_name in excel_file.sheet_names:
            # na_values='', keep_default_na=False - fixed read "null" as None
            # dtype=str - fixed read int number as float (in column must be only numbers)
            excel_sheet_data_frame = excel_file.parse(
                sheet_name,
                index_col=None,
                na_values='',
                keep_default_na=False,
                dtype=str
            )
            rows_by_sheet_name[sheet_name] = _ReadRows(sheet_name, excel_sheet_data_frame, parsing_config)
        else:
            if missing_sheet_names is None:
                missing_sheet_names = []
            missing_sheet_names.append(sheet_name)

    if bool(missing_sheet_names):
        _LogSheetNamesNotFound(missing_sheet_names)

    return rows_by_sheet_name


def _ReadRows(sheet_name: str, excel_sheet_data_frame: pandas.DataFrame, parsing_config: ParsingConfig) -> list[Row]:
    result = []

    ignore_column_name = parsing_config.ignore_column_name
    link_id_column_name = parsing_config.link_id_column_name
    field_name_column_name = parsing_config.field_name_column_name
    value_type_column_name = parsing_config.field_value_type_column_name
    field_value_column_name = parsing_config.field_value_column_name
    alias_func_arg_value_column_name = parsing_config.alias_func_arg_value_column_name
    anonym_alias_func_arg_name_by_column_name = parsing_config.anonym_alias_func_arg_name_by_column_name

    _CheckMissingColumnNames(
        sheet_name,
        excel_sheet_data_frame,
        columns=
        [
            ('ignoreColumnName', ignore_column_name, False),
            ('linkIdColumnName', link_id_column_name, False),
            ('fieldNameColumnName', field_name_column_name, False),
            ('fieldValueTypeColumnName', value_type_column_name, False),
            ('fieldValueColumnName', field_value_column_name, False),
            ('aliasFuncArgValueColumnName', alias_func_arg_value_column_name, True),
        ] + [('anonymAliasFuncArgNameByColumnName', x, False) for x in anonym_alias_func_arg_name_by_column_name.keys()]
    )

    index: int
    for index, excel_row in excel_sheet_data_frame.iterrows():
        if index < parsing_config.start_parsing_row_index:
            continue

        if not _NeedIgnoreRow(sheet_name, index, excel_row, ignore_column_name):
            link_id = _ReadCellValue(excel_row, link_id_column_name)
            field_name = _ReadCellValue(excel_row, field_name_column_name)
            field_value_type = _ReadCellValue(excel_row, value_type_column_name)
            field_value = _ReadCellValue(excel_row, field_value_column_name)

            alias_func_arg_value = None
            if alias_func_arg_value_column_name is not None:
                alias_func_arg_value = _ReadCellValue(excel_row, alias_func_arg_value_column_name)

            is_empty_row = (
                    link_id is None
                    and field_name is None
                    and field_value_type is None
                    and field_value is None
                    and alias_func_arg_value is None)

            if not is_empty_row:
                anonym_args: Optional[dict[str, str]] = \
                    __ReadAnonymArgs(excel_row, anonym_alias_func_arg_name_by_column_name)
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

    _LogIgnoreTypeShouldBeBool(sheet_name, row_index, ignore_value)
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


def _CheckMissingColumnNames(
        sheet_name: str,
        excel_sheet_data_frame: pandas.DataFrame,
        columns: list[(str, str, bool)]
):
    missing_column_description_by_column_name: Optional[dict[str, str]] = None

    for (column_description, column_name, can_be_none) in columns:
        if can_be_none and column_name is None:
            continue

        if column_name not in excel_sheet_data_frame.columns:
            if missing_column_description_by_column_name is None:
                missing_column_description_by_column_name = {}

            missing_column_description_by_column_name[column_name] = column_description

    if bool(missing_column_description_by_column_name):
        _LogMissingColumnNames(sheet_name, missing_column_description_by_column_name)


def _LogMissingColumnNames(sheet_name: str, missing_column_description_by_column_name: dict[str, str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Sheet name', 'Missing columns']

    missing_columns_pretty_table = PrettyTable()
    missing_columns_pretty_table.field_names = ['Config field name', 'Column name']
    missing_columns_pretty_table.align = 'l'

    for column_name, column_description in missing_column_description_by_column_name.items():
        missing_columns_pretty_table.add_row(
            [column_description, LogFormatter.formatErrorColor(column_name)], divider=True)

    pretty_table.add_row([sheet_name, str(missing_columns_pretty_table)])

    print(''.join([
        f'\n\t{LogFormatter.formatError("Missing column name")}',
        f'\n{str(pretty_table)}'
    ]))


def _LogIgnoreTypeShouldBeBool(sheet_name, row_index, ignore_value):
    pretty_table = PrettyTable()
    pretty_table.field_names = ["Sheet name", "Row number", "Ignore value"]

    highlighted_ignore_value = LogFormatter.formatWarningColor(ignore_value)
    row_visible_number = _ConvertIndexToVisibleNumber(row_index)
    pretty_table.add_row([sheet_name, row_visible_number, highlighted_ignore_value])

    print(''.join([
        f'\n\t{LogFormatter.formatWarning("Ignore type should be bool")}',
        f'\n\tRow will be used for parsing',
        f'\n{str(pretty_table)}'
    ]))


def _LogSheetNamesNotFound(missing_sheet_names: list[str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Sheet name']
    pretty_table.align['Sheet name'] = 'l'

    highlight_missing_sheet_names = '\n'.join([LogFormatter.formatErrorColor(x) for x in missing_sheet_names])
    pretty_table.add_row([highlight_missing_sheet_names])

    print(''.join([
        f'\n\t{LogFormatter.formatError("Missing reading excel sheet")}',
        f'\n{str(pretty_table)}'
    ]))
