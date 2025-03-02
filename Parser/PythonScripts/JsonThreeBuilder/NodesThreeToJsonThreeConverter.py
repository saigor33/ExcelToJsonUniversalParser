from typing import Optional
import Configuration.JsonOperatorType
import Configuration.ValueOperatorType
from Configuration.Config import Config
from Configuration.DelimiterPresetConfig import DelimiterPresetConfig
from JsonItemsPrinter.JsonItems.BaseJsonItem import BaseJsonItem
from JsonItemsPrinter.JsonItems.ObjectJsonItem import ObjectJsonItem
from JsonItemsPrinter.JsonItems.FieldValueJsonItem import FieldValueJsonItem
from JsonThreeBuilder.Node import Node


class Converter:
    def __init__(self, parsing_excel_config: Config.ParsingExcel, delimiter_presets: dict[str, DelimiterPresetConfig]):
        self.__parsing_excel_config = parsing_excel_config
        self.__delimiter_presets = delimiter_presets

    def convert(self, feature_name: str, node: Node) -> BaseJsonItem:
        return self.__ConvertToJsonItem(feature_name, node)

    def __ConvertToJsonItem(self, root_field_name: str, node: Node) -> BaseJsonItem:
        if node.nodes is None:
            if self.__IsValueOperator(node.field_name):
                field_name = root_field_name
                operator_type = node.field_name
                field_value = node.node_value.get()
                return FieldValueJsonItem(field_name, operator_type, field_value)
            else:
                field_name = node.field_name
                return ObjectJsonItem(field_name, None, [])
        else:
            node_field_name = node.field_name
            delimiter_preset: Optional[DelimiterPresetConfig] = None
            inner_json_items: list[BaseJsonItem] = []

            inner_node: Node
            for inner_node in node.nodes:
                if inner_node.field_name == Configuration.JsonOperatorType.LayerDelimiter:

                    if delimiter_preset is not None:
                        raise Exception("Delimiter preset already set")

                    delimiter_preset_id = inner_node.node_value.get()
                    delimiter_preset = self.__delimiter_presets[delimiter_preset_id]
                else:
                    inner_json_items.append(self.__ConvertToJsonItem(node_field_name, inner_node))

        return ObjectJsonItem(node_field_name, delimiter_preset, inner_json_items)

    @staticmethod
    def __IsValueOperator(field_value: str) -> bool:
        return (field_value == Configuration.ValueOperatorType.String
                or field_value == Configuration.ValueOperatorType.Number
                or field_value == Configuration.ValueOperatorType.Null
                or field_value == Configuration.ValueOperatorType.Bool)
