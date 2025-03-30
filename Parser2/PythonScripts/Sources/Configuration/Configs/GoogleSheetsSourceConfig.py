from Sources.Configuration.Configs.ParsingConfig import ParsingConfig


class GoogleSheetsSourceConfig:
    def __init__(
            self,
            credentials_file_path: str,
            spreadsheet_id: str,
            features_parsing: ParsingConfig,
            alias_funcs_parsing: ParsingConfig
    ):
        self.credentials_file_path = credentials_file_path
        self.spreadsheet_id = spreadsheet_id
        self.features_parsing = features_parsing
        self.alias_funcs_parsing = alias_funcs_parsing
