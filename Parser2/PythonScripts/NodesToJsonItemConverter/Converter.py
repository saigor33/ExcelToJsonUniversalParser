from prettytable import PrettyTable
import Configuration.ReferenceType
from Configuration import FieldValueType
from Json.BaseJsonItem import BaseJsonItem, ObjectJsonItem, ValueFieldJsonItem
from RowToJsonConverter import AliasFuncStackLogFormatter
from RowToJsonConverter.Node import Node
from Tests import LogFormatter


def convert(node: Node) -> BaseJsonItem:
    invalid_field_names_stacks: list[(str, bool)] = []

    is_array = \
        node.inner_nodes is not None \
        and len(node.inner_nodes) == 1 \
        and node.inner_nodes[0].value == Configuration.ReferenceType.Array

    node_to_convert: Node = node.inner_nodes[0] if is_array else node

    inner_json_items: list[BaseJsonItem] = []
    if node_to_convert.inner_nodes is not None:
        for index, inner_node in enumerate(node_to_convert.inner_nodes):
            should_be_name = not is_array
            field_names_stack: list[str] = []

            inner_json_item = \
                _ConvertInternal(inner_node, invalid_field_names_stacks, field_names_stack, should_be_name)
            inner_json_items.append(inner_json_item)

    if bool(invalid_field_names_stacks):
        feature_name = node.name
        _LogInvalidFieldNames(feature_name, invalid_field_names_stacks)

    return ObjectJsonItem(None, is_array, inner_json_items)


def _ConvertInternal(
        node: Node,
        invalid_field_names_stacks: list[(str, bool)],
        field_names_stack: list[str],
        should_be_name: bool
) -> BaseJsonItem:
    node_name = node.name
    _CheckExistName(node_name, invalid_field_names_stacks, field_names_stack, should_be_name)

    if node.inner_nodes is None:
        if node.value is not None:
            raise Exception("Unknown node type", node)
        # todo: check array
        return ObjectJsonItem(node_name, False, [])
    elif _IsValueFieldNode(node):
        value_field_node = node.inner_nodes[0]
        return ValueFieldJsonItem(node_name, value_field_node.name, value_field_node.value)
    else:
        is_array = node.value == Configuration.ReferenceType.Array
        new_should_be_name = not is_array

        inner_json_items: list[BaseJsonItem] = []
        for inner_node in node.inner_nodes:
            new_field_names_stack = field_names_stack + [node_name]
            inner_json_item = \
                _ConvertInternal(inner_node, invalid_field_names_stacks, new_field_names_stack, new_should_be_name)
            inner_json_items.append(inner_json_item)
        return ObjectJsonItem(node_name, is_array, inner_json_items)


def _CheckExistName(
        node_name: str,
        invalid_field_names_stacks: list[(str, bool)],
        field_names_stack: list[str],
        should_be_name: bool
):
    is_missing_name = should_be_name and node_name is None
    is_unused_name = not should_be_name and node_name is not None

    if is_missing_name or is_unused_name:
        highlight_node_name = LogFormatter.formatErrorColor(node_name)
        formatted_field_names_stack = AliasFuncStackLogFormatter.stackFormat(field_names_stack, highlight_node_name)
        invalid_field_names_stacks.append((formatted_field_names_stack, is_missing_name))


def _IsValueFieldNode(node: Node) -> bool:
    if node is None:
        raise Exception("Node can't be None")

    if node.inner_nodes is None:
        return False

    if len(node.inner_nodes) != 1:
        return False

    return (node.inner_nodes[0].name == FieldValueType.JsonAlias
            or node.inner_nodes[0].name == FieldValueType.String
            or node.inner_nodes[0].name == FieldValueType.Number
            or node.inner_nodes[0].name == FieldValueType.Null
            or node.inner_nodes[0].name == FieldValueType.Bool)


def _LogInvalidFieldNames(feature_name: str, invalid_field_names_stacks: list[(str, bool)]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Feature name', 'Invalid fields']
    pretty_table.align = 'l'

    invalid_fields_pretty_table = PrettyTable()
    invalid_fields_pretty_table.field_names = ['Invalid type', 'Fields names stack']
    invalid_fields_pretty_table.align = 'l'

    for invalid_field_names_stack, is_missing_name in invalid_field_names_stacks:
        invalid_type = 'Missing name' if is_missing_name else 'Unrequired name'
        invalid_fields_pretty_table.add_row([invalid_type, invalid_field_names_stack], divider=True)

    pretty_table.add_row([feature_name, str(invalid_fields_pretty_table)], divider=True)

    print(''.join([
        f'\n\t{LogFormatter.formatError("Invalid field name detect")}'
        f'\n{str(pretty_table)}'
    ]))
