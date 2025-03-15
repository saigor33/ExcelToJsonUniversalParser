import os
import sys
import time

from Configuration import FieldValueType
from Json.BaseJsonItem import ObjectJsonItem, BaseJsonItem, ValueFieldJsonItem
from Json.LayerDelimiterPreset import LayerDelimiterPreset
from Sources.Excel.Configuration.Config import Config


class Result:
    def __init__(self, output_file_path: str, duration: float):
        self.output_file_path = output_file_path
        self.duration = duration


class Printer:
    def __init__(self, padding_per_layer: str):
        self.__padding_per_layer = padding_per_layer

    def print(
            self,
            parsing_feature_config: Config.ParsingFeature,
            json_item: BaseJsonItem,
    ) -> Result:
        start_print_time = time.time()

        if not os.path.exists(parsing_feature_config.output_directory):
            os.makedirs(parsing_feature_config.output_directory)

        output_file_path = '/'.join([parsing_feature_config.output_directory, parsing_feature_config.output_file_name])

        orig_stdout = sys.stdout
        output_file = open(output_file_path, 'w')
        sys.stdout = output_file

        self._PrintInternal(json_item, 0, False)

        sys.stdout = orig_stdout
        output_file.close()

        total_print_time_duration = time.time() - start_print_time
        return Result(output_file_path, total_print_time_duration)

    def _PrintInternal(self, json_item: BaseJsonItem, layer_index: int, need_comma: bool):
        json_item_type = type(json_item)
        if json_item_type is ObjectJsonItem:
            object_json_item: ObjectJsonItem = json_item
            self._PrintObjectJsonItem(object_json_item, layer_index, need_comma)
        elif json_item_type is ValueFieldJsonItem:
            field_value_json_item: ValueFieldJsonItem = json_item
            self._PrintValueFieldJsonItem(field_value_json_item, layer_index, need_comma)
        else:
            raise Exception("Unknown JsonItem type", json_item_type)

    def _PrintObjectJsonItem(self, object_json_item: ObjectJsonItem, layer_index: int, need_comma: bool):
        # 1. root item is not has field name
        # 2. array elements does`t has field name
        if object_json_item.field_name is not None:
            self._PrintWithPadding(layer_index, "".join(["\"", object_json_item.field_name, "\"", ":"]))

        layer_delimiter_preset = self._GetLayerDelimiterPreset(object_json_item.is_array)
        self._PrintWithPadding(layer_index, layer_delimiter_preset.opening_part)

        inner_object_json_items_count = len(object_json_item.json_items)
        for i in range(inner_object_json_items_count):
            inner_json_item: BaseJsonItem = object_json_item.json_items[i]
            inner_object_need_comma = i != inner_object_json_items_count - 1
            next_layer_index = layer_index + 1
            self._PrintInternal(inner_json_item, next_layer_index, inner_object_need_comma)

        comma = "," if need_comma else ""
        self._PrintWithPadding(layer_index, ''.join([layer_delimiter_preset.closing_part, comma]))

    def _PrintValueFieldJsonItem(self, value_field_json_item: ValueFieldJsonItem, layer_index: int, need_comma: bool):
        value_builder: list[str] = []
        value_builder.append(self.__padding_per_layer * layer_index)
        if value_field_json_item.field_name is not None:
            value_builder.append("\"")
            value_builder.append(str(value_field_json_item.field_name))
            value_builder.append("\"")
            value_builder.append(":")
            value_builder.append(" ")
        if value_field_json_item.field_value_type == FieldValueType.String:
            value_builder.append("\"")
            value_builder.append(str(value_field_json_item.field_value))
            value_builder.append("\"")
        elif value_field_json_item.field_value_type == FieldValueType.Number:
            value_builder.append(str(value_field_json_item.field_value))
        elif value_field_json_item.field_value_type == FieldValueType.Null:
            value_builder.append("null")
        elif value_field_json_item.field_value_type == FieldValueType.Bool:
            field_value = str(value_field_json_item.field_value).lower()
            if field_value == "true" or field_value == "1":
                result_value = "true"
            elif field_value == "false" or field_value == "0":
                result_value = "false"
            else:
                result_value = ''.join(["<error>", field_value, "</error>"])

            value_builder.append(str(result_value))
        else:
            raise Exception('Unknown ValueFieldJsonItem field value type', value_field_json_item.field_value_type)

        if need_comma:
            value_builder.append(",")

        print("".join(value_builder))

    def _GetLayerDelimiterPreset(self, is_array: bool) -> LayerDelimiterPreset:
        return (
            LayerDelimiterPreset('[', ']')) \
            if is_array else \
            LayerDelimiterPreset('{', '}')

    def _PrintWithPadding(self, layer_index: int, text: str):
        print("".join([self.__padding_per_layer * layer_index, text]))
