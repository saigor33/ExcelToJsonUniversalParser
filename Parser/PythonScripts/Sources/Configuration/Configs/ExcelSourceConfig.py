from typing import Optional

from Sources.Configuration.Configs.ParsingConfig import ParsingConfig


class ExcelSourceConfig:
    def __init__(self, excel_file_path: str, features_parsing: ParsingConfig,
                 alias_funcs_parsing: Optional[ParsingConfig]):
        self.excel_file_path = excel_file_path
        self.features_parsing = features_parsing
        self.alias_funcs_parsing = alias_funcs_parsing
