import argparse
import time
import colorama
from prettytable import PrettyTable

import Json.Printer
import NodesToJsonItemConverter
import NodesToJsonItemConverter.Converter
from Configuration import FieldValueType
from Json.BaseJsonItem import ObjectJsonItem, ValueFieldJsonItem
from RowToJsonConverter import NodesLayerBuilder, Converter
from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer
from RowToJsonConverter.RefNodesJoiner import RefNodesJoiner
from Sources.Excel.Configuration.ConfigLoader import ConfigLoader
from Sources.Excel.Configuration.Config import Config
from Sources.Excel.Reader.Reader import Reader
from Sources.Excel.Reader.Row import Row


def main(config_file_path: str):
    benchmarks = PrettyTable()
    benchmarks.field_names = ["Step name", "Description", "Duration (seconds)"]

    start_parsing_time = time.time()

    colorama.init()

    config: Config = ConfigLoader(config_file_path).Load()

    excel_reader = Reader(config)
    ref_nodes_joiner = RefNodesJoiner()
    json_printer = Json.Printer.Printer(config.padding_per_layer)

    start_read_excel_time = time.time()
    rows_by_sheet_name: dict[str, list[Row]] = excel_reader.read()
    total_read_excel_duration = time.time() - start_read_excel_time
    benchmarks.add_row(["Read Excel", "", f"{total_read_excel_duration:.2f}"], divider=True)

    start_convert_rows_to_nodes_time = time.time()
    nodes_by_sheet_name: dict[str, list[Node]] = {}
    for sheet_name, rows in rows_by_sheet_name.items():
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

    # json_item = _GetTestJsonItem()
    print_features_benchmarks = PrettyTable()
    print_features_benchmarks.field_names = ["Feature name", "Json output path", "Duration (seconds)"]
    start_print_features_time = time.time()

    for feature_name, parsing_feature in config.parsing_features.items():
        json_item = NodesToJsonItemConverter.Converter.convert(joined_nodes_by_feature_name[feature_name])
        print_result: Json.Printer = json_printer.print(parsing_feature, json_item)
        print_features_benchmarks.add_row([feature_name, print_result.output_file_path, f"{print_result.duration:.2f}"])

    total_print_features_duration = time.time() - start_print_features_time
    print_features_benchmark = ["Print features", print_features_benchmarks, f"{total_print_features_duration:.2f}"]
    benchmarks.add_row(print_features_benchmark, divider=True)

    total_parsing_duration = time.time() - start_parsing_time
    benchmarks.add_row(["Total duration", "Total parsing duration", f"{total_parsing_duration:.2f}"], divider=True)

    print("".join([str(benchmarks)]))
    print("\nDone!")


def _GetTestJsonItem():
    return ObjectJsonItem(None, False, [
        # field values
        ValueFieldJsonItem("$type", FieldValueType.String, "TypeXXX"),
        ValueFieldJsonItem("field1", FieldValueType.Number, "12345"),
        ValueFieldJsonItem("field2", FieldValueType.Bool, "true"),
        ValueFieldJsonItem("field3", FieldValueType.Null, ""),
        # object
        ObjectJsonItem("field5", False, []),
        ObjectJsonItem("field6", False, [
            ValueFieldJsonItem("$type", FieldValueType.String, "TypeYYY")
        ]),
        # array
        ObjectJsonItem("field7", True, []),
        ObjectJsonItem("field8", True, [
            ValueFieldJsonItem(None, FieldValueType.String, "TypeYYY")
        ]),
        ObjectJsonItem("field9", True, [
            ObjectJsonItem(None, False, []),
            ObjectJsonItem(None, False, [
                ValueFieldJsonItem("$type", FieldValueType.String, "TypeYYY")
            ]),
        ]),
        # dict
        ObjectJsonItem("field10", False, [
            ValueFieldJsonItem("$dict", FieldValueType.String, "TypeZZZ"),
            ObjectJsonItem("Item1", False, []),
            ObjectJsonItem("Item2", False, []),
            ObjectJsonItem("Item3", False, []),
        ]),
    ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel to Json universal parser')
    parser.add_argument('--config_path',
                        required=True,
                        type=str,
                        help='Path to config.json')
    args = parser.parse_args()

    main(args.config_path)
