import json

from Sources.Excel.Configuration.Config import Config


class ConfigLoader:
    def __init__(self, config_file_path):
        self.__config_file_path = config_file_path

    def Load(self) -> Config:
        config_json = self.__LoadJson()

        excel_file_path: str = config_json['excelFilePath']
        padding_per_layer: str = config_json['paddingPerLayer']
        debug_config: Config.Debug = self.__LoadDebugConfig(config_json['debug'])

        parsing_excel_part_json = config_json['parsingExcel']
        parsing_excel_config: Config.Parsing = self.__LoadParsingExcelConfig(parsing_excel_part_json)

        parsing_alias_funcs_part_json = config_json['parsingAliasFuncs']
        parsing_alias_funcs_config: Config.Parsing = self.__LoadParsingExcelConfig(parsing_alias_funcs_part_json)

        parsing_feature_configs: dict[str, Config.ParsingFeature] = self.__LoadParsingFeatureConfigs(config_json)

        return Config(excel_file_path, padding_per_layer, debug_config, parsing_excel_config,
                      parsing_alias_funcs_config,
                      parsing_feature_configs)

    def __LoadJson(self):
        json_file = open(self.__config_file_path, "r")

        config_json = json.loads(json_file.read())
        json_file.close()

        return config_json

    @staticmethod
    def __LoadDebugConfig(config_json) -> Config.Debug:
        need_print_benchmarks = bool(config_json["needPrintBenchmarks"])
        return Config.Debug(need_print_benchmarks)

    @staticmethod
    def __LoadParsingFeatureConfigs(config_json) -> dict[str, Config.ParsingFeature]:
        result: dict[str, Config.ParsingFeature] = {}

        for parsing_feature_json in config_json['parsingFeatures']:
            feature_name: str = parsing_feature_json['featureName']
            output_directory: str = parsing_feature_json['outputDirectory']
            output_file_name: str = parsing_feature_json['outputFileName']

            if feature_name in result:
                raise Exception(''.join(["Feature already added (", feature_name, ")"]))

            result[feature_name] = Config.ParsingFeature(output_directory, output_file_name)

        return result

    @staticmethod
    def __LoadParsingExcelConfig(config_json) -> Config.Parsing:
        start_parsing_row_index = int(config_json['startParsingRowIndex'])
        ignore_column_index = int(config_json['ignoreColumnIndex'])
        link_id_column_index = int(config_json['linkIdColumnIndex'])
        field_name_column_index = int(config_json['fieldNameColumnIndex'])
        field_value_type_column_index = int(config_json['fieldValueTypeColumnIndex'])
        field_value_column_index = int(config_json['fieldValueColumnIndex'])
        alias_func_arg_value_column_index = int(config_json['aliasFuncArgValueColumnIndex'])
        ordered_by_level_sheet_names = config_json['orderedByLevelSheetNames']

        return Config.Parsing(
            start_parsing_row_index,
            ignore_column_index,
            link_id_column_index,
            field_name_column_index,
            field_value_type_column_index,
            field_value_column_index,
            alias_func_arg_value_column_index,
            ordered_by_level_sheet_names)
