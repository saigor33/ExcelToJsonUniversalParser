import Configuration.FieldValueType
import Configuration.ReferenceType
from RowToJsonConverter.Node import Node
from Sources.Excel.Reader.Row import Row
from prettytable import PrettyTable
from colorama import Fore, Style


def convert(sheet_name: str, rows: list[Row]) -> list[Node]:
    result: list[Node] = []

    start_block_row_index: int = 0
    last_row_index = len(rows) - 1
    for row_index in range(start_block_row_index + 1, last_row_index + 1):
        is_block_ended = row_index == last_row_index or rows[row_index + 1].link_id is not None
        if is_block_ended:
            end_block_row_index: int = row_index

            result.append(_CreateNode(sheet_name, rows, start_block_row_index, end_block_row_index))

            start_block_row_index = end_block_row_index + 1

    return result


def _CreateNode(sheet_name: str, rows, start_block_row_index, end_block_row_index):
    node_name = rows[start_block_row_index].link_id
    inner_nodes: list[Node] = []

    for block_row_index in range(start_block_row_index, end_block_row_index + 1):
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
            # todo: add empty array without ref next sheet
            ref_node = Node(Configuration.ReferenceType.Ref, row.field_value, [])
            inner_nodes.append(Node(row.field_name, field_value_type, [ref_node]))
        elif field_value_type is None:
            pass
        else:
            print(Fore.RED + 'Message: Convert row to node error' + Style.RESET_ALL)

            table = PrettyTable()
            table.field_names = ["Sheet name", "row index", "id", "name", "type", "value"]
            table.add_row(
                [sheet_name, row.original_index, row.link_id, row.field_name, field_value_type, row.field_value])
            error: list[str] = [
                '\n\tDescription: Unknown "type"',
                '\n' + str(table),
                '\n'
            ]
            print("".join(error))
    return Node(node_name, None, inner_nodes)


def _IsValueField(field_value_type):
    return field_value_type == Configuration.FieldValueType.Number \
        or field_value_type == Configuration.FieldValueType.String \
        or field_value_type == Configuration.FieldValueType.Bool \
        or field_value_type == Configuration.FieldValueType.Null
