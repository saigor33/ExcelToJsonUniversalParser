import Configuration.FieldValueType
import Configuration.ReferenceType
from RowToJsonConverter.Node import Node
from Sources.Excel.Reader.Row import Row
from prettytable import PrettyTable
from colorama import Fore, Style


def convert(sheet_name: str, rows: list[Row]) -> list[Node]:
    result: list[Node] = []

    start_block_row_index: int = 0
    row_index = start_block_row_index
    last_row_index = len(rows) - 1
    while row_index <= last_row_index:
        if row_index == last_row_index:
            result.append(_CreateNode(sheet_name, rows, start_block_row_index, last_row_index))
        elif rows[row_index + 1].link_id is not None:
            result.append(_CreateNode(sheet_name, rows, start_block_row_index, row_index))
            start_block_row_index = row_index + 1
        row_index += 1

    return result


# todo: remove sheet name
def _CreateNode(sheet_name: str, rows, start_block_row_index, end_block_row_index):
    node_name = rows[start_block_row_index].link_id
    inner_nodes: list[Node] = []

    block_row_index = start_block_row_index
    while block_row_index <= end_block_row_index:
        row = rows[block_row_index]

        field_value_type = row.field_value_type
        if _IsValueField(field_value_type):
            value_node = Node(field_value_type, row.field_value)
            node = Node(row.field_name, None, [value_node])
            inner_nodes.append(node)
        elif field_value_type == Configuration.ReferenceType.Ref:
            ref_node = Node(field_value_type, row.field_value, [])
            value_node = Node(row.field_name, None, [ref_node])
            inner_nodes.append(value_node)
        elif field_value_type == Configuration.ReferenceType.Array:
            ref_node = Node(Configuration.ReferenceType.Ref, row.field_value, [])
            inner_nodes.append(Node(row.field_name, field_value_type, [ref_node]))
        elif field_value_type is None:
            pass
        else:
            alias_func_name = field_value_type
            sub_inner_nodes: list[Node] = []
            while True:
                sub_block_row: Row = rows[block_row_index]
                alias_func_arg_name = sub_block_row.field_value
                alias_func_arg_value = sub_block_row.alias_func_arg_value

                sub_inner_nodes.append(Node(alias_func_arg_name, alias_func_arg_value, None))

                if _IsSubBlockEnded(block_row_index, end_block_row_index, rows):
                    break
                else:
                    block_row_index += 1
            func_node = Node(alias_func_name, None, sub_inner_nodes)
            inner_nodes.append(Node(row.field_name, Configuration.ReferenceType.AliasFunc, [func_node]))
        block_row_index += 1
    return Node(node_name, None, inner_nodes)


def _IsSubBlockEnded(block_row_index: int, end_block_row_index: int, rows: list[Row]) -> bool:
    if block_row_index == end_block_row_index:
        return True

    next_row = rows[block_row_index + 1]
    is_sub_block_ended = next_row.field_name is not None or next_row.field_value_type is not None
    return is_sub_block_ended


def _IsValueField(field_value_type):
    return field_value_type == Configuration.FieldValueType.Number \
        or field_value_type == Configuration.FieldValueType.String \
        or field_value_type == Configuration.FieldValueType.Bool \
        or field_value_type == Configuration.FieldValueType.Null
