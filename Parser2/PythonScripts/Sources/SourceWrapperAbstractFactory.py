from Sources.BaseSourceWrapper import BaseSourceWrapper
from Sources.Configuration.Configs.Config import Config
from Sources.Configuration.Configs.SourceType import SourceType
from Sources.Excel.SourceWrapper import SourceWrapper as ExcelSourceWrapper
from Sources.GoogleSheet.SourceWrapper import SourceWrapper as GoogleSheetSourceWrapper


def create(config: Config) -> BaseSourceWrapper:
    selected_source_type: SourceType = config.selected_source_type

    if selected_source_type == SourceType.Excel:
        return ExcelSourceWrapper(config.excel_source)

    if selected_source_type == SourceType.GoogleSheet:
        return GoogleSheetSourceWrapper(config.google_sheets_source)

    raise ValueError(f'Unsupported source type: {selected_source_type}')
