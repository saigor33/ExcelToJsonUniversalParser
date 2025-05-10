import json
from Sources.Configuration.Configs.Config import Config
from Sources.Configuration.Configs.DebugConfig import DebugConfig
from Sources.Configuration.Configs.ExcelSourceConfig import ExcelSourceConfig
from Sources.Configuration.Configs.GoogleSheetsSourceConfig import GoogleSheetsSourceConfig
from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.Configuration.Configs.ParsingFeatureConfig import ParsingFeatureConfig
from Sources.Configuration.Configs.SourceType import SourceType


class ConfigLoader:
    def __init__(self, config_file_path):
        self.__config_file_path = config_file_path

    def Load(self) -> Config:
        config_json = self.__LoadJson()

        padding_per_layer: str = config_json['paddingPerLayer']
        debug_config: DebugConfig = self.__LoadDebugConfig(config_json['debug'])
        selected_source_type: SourceType = self.__LoadSourceType(config_json['selectedSourceType'])
        excel_source_config = self.__LoadExcelSourceConfig(config_json['excelSource'])
        google_sheets_source_config = self.__LoadGoogleSheetsSourceConfig(config_json['googleSheetsSource'])

        parsing_feature_configs: dict[str, ParsingFeatureConfig] = self.__LoadParsingFeatureConfigs(config_json)

        return Config(padding_per_layer, debug_config, selected_source_type, excel_source_config,
                      google_sheets_source_config, parsing_feature_configs)

    def __LoadJson(self):
        json_file = open(self.__config_file_path, "r")

        config_json = json.loads(json_file.read())
        json_file.close()

        return config_json

    def __LoadExcelSourceConfig(self, config_json) -> ExcelSourceConfig:
        excel_file_path: str = config_json['excelFilePath']
        features_parsing_config: ParsingConfig = self.__LoadParsingConfig(config_json['featuresParsing'])
        alias_funcs_parsing_config: ParsingConfig = self.__LoadParsingConfig(config_json['aliasFuncsParsing'])

        return ExcelSourceConfig(excel_file_path, features_parsing_config, alias_funcs_parsing_config)

    def __LoadGoogleSheetsSourceConfig(self, config_json) -> GoogleSheetsSourceConfig:
        credentials_file_path: str = config_json['credentialsFilePath']
        spreadsheet_id: str = config_json['spreadsheetId']
        features_parsing_config: ParsingConfig = self.__LoadParsingConfig(config_json['featuresParsing'])
        alias_funcs_parsing_config: ParsingConfig = self.__LoadParsingConfig(config_json['aliasFuncsParsing'])

        return GoogleSheetsSourceConfig(credentials_file_path, spreadsheet_id, features_parsing_config,
                                        alias_funcs_parsing_config)

    @staticmethod
    def __LoadSourceType(str_source_type: str) -> SourceType:
        if str_source_type == 'GoogleSheets':
            return SourceType.GoogleSheet
        if str_source_type == 'Excel':
            return SourceType.Excel

        raise ValueError(f'Unknown source type {str_source_type}')

    @staticmethod
    def __LoadDebugConfig(config_json) -> DebugConfig:
        need_print_benchmarks = bool(config_json["needPrintBenchmarks"])
        return DebugConfig(need_print_benchmarks)

    @staticmethod
    def __LoadParsingFeatureConfigs(config_json) -> dict[str, ParsingFeatureConfig]:
        result: dict[str, ParsingFeatureConfig] = {}

        for parsing_feature_json in config_json['parsingFeatures']:
            feature_name: str = parsing_feature_json['featureName']
            output_directory: str = parsing_feature_json['outputDirectory']
            output_file_name: str = parsing_feature_json['outputFileName']

            if feature_name in result:
                raise Exception(''.join(["Feature already added (", feature_name, ")"]))

            result[feature_name] = ParsingFeatureConfig(output_directory, output_file_name)

        return result

    @staticmethod
    def __LoadParsingConfig(config_json) -> ParsingConfig:
        start_parsing_row_index = int(config_json['startParsingRowIndex'])
        ignore_column_name = str(config_json['ignoreColumnName'])
        link_id_column_name = str(config_json['linkIdColumnName'])
        field_name_column_name = str(config_json['fieldNameColumnName'])
        field_value_type_column_name = str(config_json['fieldValueTypeColumnName'])
        field_value_column_name = str(config_json['fieldValueColumnName'])
        alias_func_arg_value_column_name = str(config_json['aliasFuncArgValueColumnName'])
        ordered_by_level_sheet_names = config_json['orderedByLevelSheetNames']

        return ParsingConfig(
            start_parsing_row_index,
            ignore_column_name,
            link_id_column_name,
            field_name_column_name,
            field_value_type_column_name,
            field_value_column_name,
            alias_func_arg_value_column_name,
            ordered_by_level_sheet_names)
