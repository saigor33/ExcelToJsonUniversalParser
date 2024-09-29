import Configuration.ValueOperatorType
from JsonItemsPrinter.JsonItems.FieldValueJsonItem import FieldValueJsonItem
from JsonItemsPrinter.JsonItems.ObjectJsonItem import ObjectJsonItem


class Printer:
    def __init__(self, padding_per_layer):
        self.__padding_per_layer = padding_per_layer

    def print(self, json_item):
        layer_index = 0
        need_comma = False
        self.__ParseInternal(json_item, layer_index, need_comma)

    def __ParseInternal(self, json_item, layer_index, need_comma):
        json_item_type = type(json_item)
        if json_item_type is ObjectJsonItem:
            object_json_item = json_item

            # 1. root item is not has field name
            # 2. array elements does`t has field name
            if object_json_item.field_name is not None:
                print("".join([self.__padding_per_layer * layer_index, "\"", object_json_item.field_name, "\"", ":"]))

            if object_json_item.delimiter_preset is not None:
                print(''.join([self.__padding_per_layer * layer_index, object_json_item.delimiter_preset.opening_part]))

            inner_object_json_items_count = len(object_json_item.json_items)
            for i in range(inner_object_json_items_count):
                inner_json_item = object_json_item.json_items[i]
                inner_object_need_comma = i != inner_object_json_items_count - 1
                next_layer_index = layer_index + 1
                self.__ParseInternal(inner_json_item, next_layer_index, inner_object_need_comma)

            if object_json_item.delimiter_preset is not None:
                comma = "," if need_comma else ""
                print(''.join(
                    [self.__padding_per_layer * layer_index, object_json_item.delimiter_preset.closing_part, comma]))
        elif json_item_type is FieldValueJsonItem:

            field_value_json_item = json_item
            value_builder = []
            value_builder.append(self.__padding_per_layer * layer_index)
            if field_value_json_item.field_name is not None:
                value_builder.append("\"")
                value_builder.append(str(field_value_json_item.field_name))
                value_builder.append("\"")
                value_builder.append(":")
                value_builder.append(" ")
            if field_value_json_item.operator_type == Configuration.ValueOperatorType.String:
                value_builder.append("\"")
                value_builder.append(str(field_value_json_item.field_value))
                value_builder.append("\"")
            elif field_value_json_item.operator_type == Configuration.ValueOperatorType.Number:
                value_builder.append(str(field_value_json_item.field_value))
            elif field_value_json_item.operator_type == Configuration.ValueOperatorType.Null:
                value_builder.append("null")
            else:
                raise Exception("".join(['Unknown operator type (', str(field_value_json_item.operator_type), ")"]))

            if need_comma:
                value_builder.append(",")

            print("".join(value_builder))

        else:
            raise Exception("".join(['JsonItem parse error (', str(json_item_type), ")"]))
