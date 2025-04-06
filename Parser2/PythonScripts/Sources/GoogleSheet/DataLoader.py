from typing import Optional

import googleapiclient
import googleapiclient.discovery
from google.oauth2 import service_account
from Sources.GoogleSheet.RangeConfig import RangeConfig


def load(
        credentials_file_name: str,
        spreadsheet_id: str,
        range_configs: list[RangeConfig]
) -> dict[str, list[str]]:
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    credentials = service_account.Credentials.from_service_account_file(credentials_file_name, scopes=scopes)
    sheets_service = googleapiclient.discovery.build(serviceName='sheets', version='v4', credentials=credentials)

    # todo: validate permission on GoogleSheets Api
    # todo: validate permission Google Sheets file
    # todo: validate sheet name exist

    range_names = _CollectFormatedRanges(range_configs)

    result = (
        sheets_service
        .spreadsheets()
        .values()
        .batchGet(spreadsheetId=spreadsheet_id, ranges=range_names)
        .execute()
    )
    ranges = result.get("valueRanges", [])

    parsed_result = {}
    for range in ranges:
        modified_range_name = range['range']
        range_id = _FindRangeId(modified_range_name, range_configs)

        if range_id is not None:
            parsed_result[range_id] = range['values'] if 'values' in range else []
        else:
            print("Range not found", modified_range_name)  # table logs

    return parsed_result


def _FindRangeId(modified_range_name, range_configs: list[RangeConfig]) -> Optional[str]:
    sheet_name_separator_index = modified_range_name.find('!')
    if sheet_name_separator_index == -1:
        print("Sheet name separator '!' not found", modified_range_name)  # table logs
        return None

    sheet_name = modified_range_name[:sheet_name_separator_index]
    columns_range = modified_range_name[sheet_name_separator_index + 1:]

    range_separator_index = columns_range.find(':')
    if range_separator_index == -1:
        print("Range separator '!' not found", modified_range_name)  # table logs
        return None

    start_cell = columns_range[:range_separator_index]
    end_cell = columns_range[range_separator_index + 1:]

    for range_config in range_configs:
        if sheet_name == range_config.sheet_name or sheet_name == f"'{range_config.sheet_name}'":
            range_config_start_cell = f"{range_config.start_column_name}{range_config.start_row_index}"
            if (start_cell == range_config_start_cell
                    and end_cell.startswith(range_config.end_column_name)):
                return range_config.id

    return None


def _CollectFormatedRanges(range_configs: list[RangeConfig]) -> list[str]:
    result = []
    for range_config in range_configs:
        result.append(_FormatRange(range_config))

    return result


def _FormatRange(range_config: RangeConfig) -> str:
    sheet_name = range_config.sheet_name

    formated_sheet_name = sheet_name if sheet_name.find(' ') == -1 else f'{sheet_name}'
    start_range = f"{range_config.start_column_name}{range_config.start_row_index}"
    end_row_index = range_config.end_row_index
    end_range = f"{range_config.end_column_name}{end_row_index if end_row_index is not None else ''}"

    return f"{formated_sheet_name}!{start_range}:{end_range}"
