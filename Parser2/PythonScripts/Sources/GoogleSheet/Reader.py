from typing import Optional

from colorama import Fore, Style
from prettytable import PrettyTable

from Sources import Row
from Sources.GoogleSheet import DataLoader
from Sources.GoogleSheet.RangeConfig import RangeConfig


class SheetConfig:
    def __init__(
            self,
            start_parsing_row_index: int,
            ignore_column_name: str,
            link_id_column_name: str,
            field_name_column_name: str,
            field_value_type_column_name: str,
            field_value_column_name: str,
            alias_func_arg_value_column_name: str
    ):
        self.start_parsing_row_index = start_parsing_row_index
        self.ignore_column_name = ignore_column_name
        self.link_id_column_name = link_id_column_name
        self.field_name_column_name = field_name_column_name
        self.field_value_type_column_name = field_value_type_column_name
        self.field_value_column_name = field_value_column_name
        self.alias_func_arg_value_column_name = alias_func_arg_value_column_name


def read(
        credentials_file_name: str,
        spreadsheet_id: str,
        sheet_configs_by_sheet_name: dict[str, SheetConfig]
) -> dict[str, list[Row]]:
    range_configs: list[RangeConfig] = _GenerateRangeConfigs(sheet_configs_by_sheet_name)
    sheet_data_by_range_id: dict[str, list[str]] = DataLoader.load(credentials_file_name, spreadsheet_id, range_configs)

    rows_by_sheet_name: dict[str, list[Row]] = \
        CovertDataToRow(sheet_configs_by_sheet_name, range_configs, sheet_data_by_range_id)
    return rows_by_sheet_name


def _GetRangeValues(range_configs: list[RangeConfig], sheet_name: str, column_name: str,
                    sheet_data_by_range_id: dict[str, list[str]]):
    for range_config in range_configs:
        if range_config.sheet_name == sheet_name and range_config.start_column_name == column_name:
            return sheet_data_by_range_id[range_config.id]

    raise Exception("Range values not found", sheet_name, range_configs, column_name)


def CovertDataToRow(sheet_configs_by_sheet_name: dict[str, SheetConfig], range_configs: list[RangeConfig],
                    sheet_data_by_range_config_id) -> dict[str, list[Row]]:
    rows_by_sheet_name: dict[str, list[Row]] = {}

    for sheet_name, sheet_config in sheet_configs_by_sheet_name.items():
        ignore_column_name = sheet_config.ignore_column_name
        link_id_column_name = sheet_config.link_id_column_name
        field_name_column_name = sheet_config.field_name_column_name
        value_type_column_name = sheet_config.field_value_type_column_name
        field_value_column_name = sheet_config.field_value_column_name
        arg_value_column_name = sheet_config.alias_func_arg_value_column_name

        ignore_rows_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, ignore_column_name, sheet_data_by_range_config_id)
        link_id_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, link_id_column_name, sheet_data_by_range_config_id)
        field_name_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, field_name_column_name, sheet_data_by_range_config_id)
        field_value_type_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, value_type_column_name, sheet_data_by_range_config_id)
        field_value_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, field_value_column_name, sheet_data_by_range_config_id)
        alias_func_arg_value_range: list[str] = \
            _GetRangeValues(range_configs, sheet_name, arg_value_column_name, sheet_data_by_range_config_id)

        max_rows_count = max(
            len(ignore_rows_range),
            len(link_id_range),
            len(field_name_range),
            len(field_value_type_range),
            len(field_value_range),
            len(alias_func_arg_value_range)
        )

        rows: list[Row] = []
        for row_index in range(max_rows_count):
            if not _NeedIgnoreRow(sheet_name, ignore_rows_range, row_index):
                link_id = _ReadCellValue(link_id_range, row_index)
                field_name = _ReadCellValue(field_name_range, row_index)
                field_value_type = _ReadCellValue(field_value_type_range, row_index)
                field_value = _ReadCellValue(field_value_range, row_index)
                alias_func_arg_value = _ReadCellValue(alias_func_arg_value_range, row_index)

                is_empty_row = (
                        link_id is None
                        and field_name is None
                        and field_value_type is None
                        and field_value is None
                        and alias_func_arg_value is None)

                if not is_empty_row:
                    row = Row.Row(row_index, link_id, field_name, field_value_type, field_value, alias_func_arg_value)
                    rows.append(row)

        rows_by_sheet_name[sheet_name] = rows
    return rows_by_sheet_name


def _GenerateRangeConfigs(sheet_configs_by_sheet_name: dict[str, SheetConfig]) -> list[RangeConfig]:
    result = []
    for sheet_name, sheet_config in sheet_configs_by_sheet_name.items():
        start_index = sheet_config.start_parsing_row_index

        ignore_column_name = sheet_config.ignore_column_name
        link_id_column_name = sheet_config.link_id_column_name
        field_name_column_name = sheet_config.field_name_column_name
        value_type_column_name = sheet_config.field_value_type_column_name
        field_value_column_name = sheet_config.field_value_column_name
        arg_value_column_name = sheet_config.alias_func_arg_value_column_name

        result.append(_GenerateRangeConfig(sheet_name, ignore_column_name, ignore_column_name, start_index))
        result.append(_GenerateRangeConfig(sheet_name, link_id_column_name, link_id_column_name, start_index))
        result.append(_GenerateRangeConfig(sheet_name, field_name_column_name, field_name_column_name, start_index))
        result.append(_GenerateRangeConfig(sheet_name, value_type_column_name, value_type_column_name, start_index))
        result.append(_GenerateRangeConfig(sheet_name, field_value_column_name, field_value_column_name, start_index))
        result.append(_GenerateRangeConfig(sheet_name, arg_value_column_name, arg_value_column_name, start_index))

    return result


def _GenerateRangeConfig(sheet_name: str, start_column_name: str, end_column_name: str,
                         start_row_index: int) -> RangeConfig:
    config_id = f"{sheet_name}!{start_column_name}{start_row_index}:{end_column_name}"
    return RangeConfig(config_id, sheet_name, start_column_name, end_column_name, start_row_index, end_row_index=None)


def _NeedIgnoreRow(sheet_name: str, ignore_rows_range: list[str], row_index: int):
    ignore_value = _ReadCellValue(ignore_rows_range, row_index)

    if ignore_value is None:
        return False

    ignore_value = ignore_value.lower()
    if ignore_value == 'true' or ignore_value == '1' or ignore_value == '1.0':
        return True
    if ignore_value == 'false' or ignore_value == '0' or ignore_value == '0.0':
        return False

    print(f"{Fore.YELLOW}Warning: ignore type should be bool.{Style.RESET_ALL}")

    table = PrettyTable()
    table.field_names = ["Sheet name", "Row index", "ignore", ]
    highlighted_ignore_value = "".join([Fore.YELLOW, ignore_value, Style.RESET_ALL])
    table.add_row([sheet_name, row_index, highlighted_ignore_value])

    print(f"{str(table)}\n")
    return False


def _ReadCellValue(rows_range, row_index) -> Optional[str]:
    if len(rows_range) <= row_index:
        return None

    values_count = len(rows_range[row_index])
    if values_count == 0:
        return None

    if values_count > 1:
        raise Exception("Unsupported number of rows", values_count)

    return rows_range[row_index][0].strip()
