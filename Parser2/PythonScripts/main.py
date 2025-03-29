import argparse
import time
import colorama
from prettytable import PrettyTable

import Json.Printer
import NodesToJsonItemConverter
import NodesToJsonItemConverter.Converter
from RowToJsonConverter import NodesLayerBuilder, Converter, AliasFuncNodesJoiner
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer
from RowToJsonConverter.RefNodesJoiner import RefNodesJoiner
from Sources.Excel.Configuration.ConfigLoader import ConfigLoader
from Sources.Excel.Configuration.Config import Config
import Sources.Excel.Reader.Reader as ExcelReader
from Sources.Excel.Reader.Row import Row


def main(config_file_path: str):
    benchmarks = PrettyTable()
    benchmarks.field_names = ["Step name", "Description", "Duration (seconds)"]

    start_parsing_time = time.time()

    colorama.init()

    config: Config = ConfigLoader(config_file_path).Load()

    ref_nodes_joiner = RefNodesJoiner()
    json_printer = Json.Printer.Printer(config.padding_per_layer)

    # ===============
    # todo: add benchmaerk
    alias_func_rows_by_sheet_name: dict[str, list[Row]] = (
        ExcelReader.read(config.excel_file_path, config.alias_funcs_parsing))

    alias_func_nodes_by_sheet_name: dict[str, list[Node]] = {}
    for sheet_name, rows in alias_func_rows_by_sheet_name.items():
        alias_func_nodes_by_sheet_name[sheet_name] = Converter.convert(sheet_name, rows)

    alias_func_nodes_layer: NodesLayer = NodesLayerBuilder.build(
        config.alias_funcs_parsing.ordered_by_level_sheet_names,
        alias_func_nodes_by_sheet_name)

    joined_nodes_by_alias_func_signature: dict[str, Node] = {}
    for alias_func_node in alias_func_nodes_layer.nodes:
        alias_func_signature = alias_func_node.name
        joined_nodes_by_alias_func_signature[alias_func_signature] = (
            ref_nodes_joiner.join(alias_func_node, alias_func_nodes_layer.next_nodes_layer))

    alias_func_resolver = AliasFuncResolver(joined_nodes_by_alias_func_signature)
    # =============

    start_read_excel_time = time.time()
    features_rows_by_sheet_name: dict[str, list[Row]] = ExcelReader.read(config.excel_file_path, config.parsing)
    total_read_excel_duration = time.time() - start_read_excel_time
    benchmarks.add_row(["Read Excel", "", f"{total_read_excel_duration:.2f}"], divider=True)

    start_convert_rows_to_nodes_time = time.time()
    nodes_by_sheet_name: dict[str, list[Node]] = {}
    for sheet_name, rows in features_rows_by_sheet_name.items():
        nodes_by_sheet_name[sheet_name] = Converter.convert(sheet_name, rows)
    total_convert_rows_to_nodes_duration = time.time() - start_convert_rows_to_nodes_time
    benchmarks.add_row(["Covert excel rows", "", f"{total_convert_rows_to_nodes_duration:.2f}"], divider=True)

    nodes_layer: NodesLayer = NodesLayerBuilder.build(config.parsing.ordered_by_level_sheet_names, nodes_by_sheet_name)

    start_join_nodes_by_feature_time = time.time()
    joined_nodes_by_feature_name: dict[str, Node] = {}
    for node in nodes_layer.nodes:
        feature_name = node.name
        if feature_name in config.parsing_features:
            joined_nodes_by_feature_name[feature_name] = ref_nodes_joiner.join(node, nodes_layer.next_nodes_layer)
    total_join_nodes_by_feature_duration = time.time() - start_join_nodes_by_feature_time
    benchmarks.add_row(["Join nodes", "", f"{total_join_nodes_by_feature_duration:.2f}"], divider=True)

    prepared_nodes_by_feature: dict[str, Node] = {}
    for feature_name, node in joined_nodes_by_feature_name.items():
        alias_func_stack = []
        prepared_node = AliasFuncNodesJoiner.join(feature_name, node, alias_func_resolver, alias_func_stack)
        prepared_nodes_by_feature[feature_name] = prepared_node

    print_features_benchmarks = PrettyTable()
    print_features_benchmarks.field_names = ["Feature name", "Json output path", "Duration (seconds)"]
    start_print_features_time = time.time()

    for feature_name, parsing_feature in config.parsing_features.items():
        json_item = NodesToJsonItemConverter.Converter.convert(prepared_nodes_by_feature[feature_name])
        print_result: Json.Printer = json_printer.print(parsing_feature, json_item)
        print_features_benchmarks.add_row([feature_name, print_result.output_file_path, f"{print_result.duration:.2f}"])

    total_print_features_duration = time.time() - start_print_features_time
    print_features_benchmark = ["Print features", print_features_benchmarks, f"{total_print_features_duration:.2f}"]
    benchmarks.add_row(print_features_benchmark, divider=True)

    total_parsing_duration = time.time() - start_parsing_time
    benchmarks.add_row(["Total duration", "Total parsing duration", f"{total_parsing_duration:.2f}"], divider=True)

    print("".join([str(benchmarks)]))
    print("\nDone!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel to Json universal parser')
    parser.add_argument('--config_path',
                        required=True,
                        type=str,
                        help='Path to config.json')
    args = parser.parse_args()

    main(args.config_path)
