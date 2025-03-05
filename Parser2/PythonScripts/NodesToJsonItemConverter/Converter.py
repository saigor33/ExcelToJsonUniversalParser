import Configuration.ReferenceType
from Configuration import FieldValueType
from Json.BaseJsonItem import BaseJsonItem, ObjectJsonItem, ValueFieldJsonItem
from RowToJsonConverter.Node import Node


def convert(node: Node) -> BaseJsonItem:
    # todo: check array
    inner_json_items: list[BaseJsonItem] = []
    if node.inner_nodes is not None:
        for index, inner_node in enumerate(node.inner_nodes):
            inner_json_items.append(_ConvertInternal(inner_node))

    return ObjectJsonItem(None, False, inner_json_items)


def _ConvertInternal(node: Node) -> BaseJsonItem:
    if node.inner_nodes is None:
        if node.value is not None:
            raise Exception("Unknown node type", node)
        # todo: check array
        return ObjectJsonItem(node.name, False, [])
    elif _IsValueFieldNode(node):
        value_field_node = node.inner_nodes[0]
        return ValueFieldJsonItem(node.name, value_field_node.name, value_field_node.value)
    else:
        is_array = node.value == Configuration.ReferenceType.Array
        inner_json_items: list[BaseJsonItem] = []
        for inner_node in node.inner_nodes:
            inner_json_items.append(_ConvertInternal(inner_node))
        return ObjectJsonItem(node.name, is_array, inner_json_items)


def _IsValueFieldNode(node: Node) -> bool:
    if node is None:
        raise Exception("Node can't be None")

    if node.inner_nodes is None:
        return False

    if len(node.inner_nodes) != 1:
        return False

    return (node.inner_nodes[0].name == FieldValueType.String
            or node.inner_nodes[0].name == FieldValueType.Number
            or node.inner_nodes[0].name == FieldValueType.Null
            or node.inner_nodes[0].name == FieldValueType.Bool)
