from Sources.BaseSourceWrapper import BaseSourceWrapper
from Sources.Configuration.Configs.GoogleSheetsSourceConfig import GoogleSheetsSourceConfig
from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.GoogleSheet import Reader as GoogleSheetReader
from Sources.GoogleSheet.Reader import SheetConfig
from Sources.Row import Row


class SourceWrapper(BaseSourceWrapper):
    def __init__(self, source_config: GoogleSheetsSourceConfig):
        self.__source_config = source_config

    def getFeaturesParsingConfig(self) -> ParsingConfig:
        return self.__source_config.features_parsing

    def getAliasFuncsParsingConfig(self):
        return self.__source_config.alias_funcs_parsing

    def read(self, parsing_config: ParsingConfig) -> dict[str, list[Row]]:
        sheet_configs_by_sheet_name: dict[str, SheetConfig] = {}
        for sheet_name in parsing_config.ordered_by_level_sheet_names:
            sheet_configs_by_sheet_name[sheet_name] = SheetConfig(
                start_parsing_row_index=parsing_config.start_parsing_row_index,
                ignore_column_name=parsing_config.ignore_column_name,
                link_id_column_name=parsing_config.link_id_column_name,
                field_name_column_name=parsing_config.field_name_column_name,
                field_value_type_column_name=parsing_config.field_value_type_column_name,
                field_value_column_name=parsing_config.field_value_column_name,
                alias_func_arg_value_column_name=parsing_config.alias_func_arg_value_column_name,
                anonym_alias_func_arg_name_by_column_name=parsing_config.anonym_alias_func_arg_name_by_column_name
            )

        return GoogleSheetReader.read(
            self.__source_config.credentials_file_path,
            self.__source_config.spreadsheet_id,
            sheet_configs_by_sheet_name
        )
