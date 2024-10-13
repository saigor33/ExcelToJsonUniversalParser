import argparse
import ExcelDataReader.Reader
import JsonItemsPrinter.Printer
import JsonThreeBuilder.Builder
import JsonThreeBuilder.JsonNodesJoiner
import JsonThreeBuilder.NodesThreeBuilder
import JsonThreeBuilder.NodesThreeToJsonThreeConverter
from Configuration.ConfigLoader import ConfigLoader
from Configuration.DelimiterPresetConfig import DelimiterPresetConfig
from FeatureParser import FeatureParser


def GroupFeatureNamesByExcelSheetName(config):
    result = {}
    for feature_name, parsing_feature_config in config.parsing_features_by_feature_name.items():
        if parsing_feature_config.excel_sheet_name not in result:
            result[parsing_feature_config.excel_sheet_name] = []

        result[parsing_feature_config.excel_sheet_name].append(feature_name)

    return result


def main(config_file_path: str):
    delimiter_preset_configs = \
        {
            '[': DelimiterPresetConfig('[', ']'),
            '{': DelimiterPresetConfig('{', '}')
        }

    config = ConfigLoader(config_file_path).Load()

    excel_data_reader = ExcelDataReader.Reader.Reader(config.parsing_excel_config, config.excel_file_path)

    nodes_three_builder = JsonThreeBuilder.NodesThreeBuilder.Builder(config.parsing_excel_config)
    nodes_three_to_json_three_converter = JsonThreeBuilder.NodesThreeToJsonThreeConverter \
        .Converter(config.parsing_excel_config, delimiter_preset_configs)
    json_nodes_joiner = JsonThreeBuilder.JsonNodesJoiner.Joiner()
    json_three_builder = JsonThreeBuilder.Builder.Builder(
        nodes_three_builder, nodes_three_to_json_three_converter, json_nodes_joiner)
    json_items_printer = JsonItemsPrinter.Printer.Printer(config.padding_per_layer)

    feature_parser = FeatureParser(json_three_builder, json_items_printer)

    feature_names_by_excel_sheet_name = GroupFeatureNamesByExcelSheetName(config)
    parsed_excel_rows_by_feature_name = excel_data_reader.read(feature_names_by_excel_sheet_name)
    for feature_name, parsed_excel_rows in parsed_excel_rows_by_feature_name.items():
        parsing_feature_config = config.parsing_features_by_feature_name[feature_name]
        feature_parser.parse(parsing_feature_config, feature_name, parsed_excel_rows)

    print("\nDone!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel to Json universal parser')
    parser.add_argument('--config_path',
                        required=True,
                        type=str,
                        help='Path to config.json')
    args = parser.parse_args()

    main(args.config_path)
