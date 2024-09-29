import json
from Configuration.Config import Config


class ConfigLoader:
    def __init__(self, config_file_path):
        self.__config_file_path = config_file_path

    def Load(self):
        config_json = self.__LoadJson()

        excel_file_path = config_json['excelFilePath']
        padding_per_layer = config_json['paddingPerLayer']
        parsing_excel_config = self.__LoadParsingExcelConfig(config_json)
        parsing_feature_configs = self.__LoadParsingFeatureConfigs(config_json)

        return Config(excel_file_path, padding_per_layer, parsing_excel_config, parsing_feature_configs)

    def __LoadJson(self):
        json_file = open(self.__config_file_path, "r")

        config_json = json.loads(json_file.read())
        json_file.close()

        return config_json

    @staticmethod
    def __LoadParsingFeatureConfigs(config_json):
        result = {}

        for parsing_feature_json in config_json['parsingFeatures']:
            excel_sheet_name = parsing_feature_json['excelSheetName']
            feature_name = parsing_feature_json['featureName']
            output_directory = parsing_feature_json['outputDirectory']
            output_file_name = parsing_feature_json['outputFileName']

            if feature_name in result:
                raise Exception(''.join(["Feature already added (", feature_name, ")"]))

            result[feature_name] = Config.ParsingFeature(excel_sheet_name, output_directory, output_file_name)

        return result

    @staticmethod
    def __LoadParsingExcelConfig(config_json):
        parsing_excel_part_json = config_json['parsingExcel']
        first_column_index = parsing_excel_part_json['firstColumnIndex']
        second_column_index = parsing_excel_part_json['secondColumnIndex']
        value_column_index = parsing_excel_part_json['valueColumnIndex']
        fields_separator = parsing_excel_part_json['fieldsSeparator']

        return Config.ParsingExcel(first_column_index, second_column_index, value_column_index, fields_separator)
