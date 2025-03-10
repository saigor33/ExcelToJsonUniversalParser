import argparse
from typing import Dict, List

import colorama

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
    colorama.init()

    config: Config = ConfigLoader(config_file_path).Load()

    excel_reader = Reader(config)
    ref_nodes_joiner = RefNodesJoiner()
    json_printer = Json.Printer.Printer(config.padding_per_layer)

    rows_by_sheet_name: dict[str, list[Row]] = excel_reader.read()

    nodes_by_sheet_name: dict[str, list[Node]] = {}
    for sheet_name, rows in rows_by_sheet_name.items():
        nodes_by_sheet_name[sheet_name] = Converter.convert(sheet_name, rows)

    nodes_layer: NodesLayer = NodesLayerBuilder.build(config.parsing.ordered_by_level_sheet_names, nodes_by_sheet_name)

    joined_nodes_by_feature_name: dict[str, Node] = {}
    for node in nodes_layer.nodes:
        feature_name = node.name
        if feature_name in config.parsing_features:
            joined_nodes_by_feature_name[feature_name] = ref_nodes_joiner.join(node, nodes_layer.next_nodes_layer)

    # json_item = _GetTestJsonItem()
    for feature_name, parsing_feature in config.parsing_features.items():
        json_item = NodesToJsonItemConverter.Converter.convert(joined_nodes_by_feature_name[feature_name])
        json_printer.print(feature_name, parsing_feature, json_item)

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
