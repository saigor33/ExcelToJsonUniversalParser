from Sources.Configuration.Configs.DebugConfig import DebugConfig
from Sources.Configuration.Configs.ExcelSourceConfig import ExcelSourceConfig
from Sources.Configuration.Configs.GoogleSheetsSourceConfig import GoogleSheetsSourceConfig
from Sources.Configuration.Configs.ParsingFeatureConfig import ParsingFeatureConfig
from Sources.Configuration.Configs.SourceType import SourceType


class Config:
    def __init__(self,
                 padding_per_layer: str,
                 debug: DebugConfig,
                 selected_source_type: SourceType,
                 excel_source: ExcelSourceConfig,
                 google_sheets_source: GoogleSheetsSourceConfig,
                 parsing_features: dict[str, ParsingFeatureConfig]):
        self.padding_per_layer = padding_per_layer
        self.debug = debug
        self.selected_source_type = selected_source_type
        self.excel_source = excel_source
        self.google_sheets_source = google_sheets_source
        self.parsing_features = parsing_features
