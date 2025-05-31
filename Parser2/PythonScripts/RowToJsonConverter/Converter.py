import Configuration.FieldValueType
from prettytable import PrettyTable
import Configuration.ReferenceType
from typing import Optional
from RowToJsonConverter.Node import Node
from Sources.Row import Row
from Tests import LogFormatter


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
            start_sub_block_visible_number = rows[block_row_index].visible_number

            applied_anonym_args_visible_number: Optional[int] = None
            ignore_anonym_args_by_visible_number: Optional[dict[int, dict[str, str]]] = None
            while True:
                sub_block_row = rows[block_row_index]
                if sub_block_row.anonym_args is not None:
                    if applied_anonym_args_visible_number is None:
                        for anonym_arg_name, anonym_arg_value in sub_block_row.anonym_args.items():
                            sub_inner_nodes.append(Node(anonym_arg_name, anonym_arg_value, None))
                        applied_anonym_args_visible_number = sub_block_row.visible_number
                    else:
                        if ignore_anonym_args_by_visible_number is None:
                            ignore_anonym_args_by_visible_number = {}
                        ignore_anonym_args_by_visible_number[sub_block_row.visible_number] = sub_block_row.anonym_args

                alias_func_arg_name = sub_block_row.field_value
                alias_func_arg_value = sub_block_row.alias_func_arg_value

                sub_inner_nodes.append(Node(alias_func_arg_name, alias_func_arg_value, None))

                if _IsSubBlockEnded(block_row_index, end_block_row_index, rows):
                    break
                else:
                    block_row_index += 1
            func_node = Node(alias_func_name, None, sub_inner_nodes)
            inner_nodes.append(Node(row.field_name, Configuration.ReferenceType.AliasFunc, [func_node]))

            end_sub_block_visible_number = rows[block_row_index].visible_number

            if bool(ignore_anonym_args_by_visible_number):
                __LogTwiceAddAnonymArgs(sheet_name, start_sub_block_visible_number, end_sub_block_visible_number,
                                        applied_anonym_args_visible_number, ignore_anonym_args_by_visible_number)

        block_row_index += 1
    return Node(node_name, None, inner_nodes)


def _IsSubBlockEnded(block_row_index: int, end_block_row_index: int, rows: list[Row]) -> bool:
    if block_row_index == end_block_row_index:
        return True

    next_row = rows[block_row_index + 1]
    is_sub_block_ended = next_row.field_name is not None or next_row.field_value_type is not None
    return is_sub_block_ended


def _IsValueField(field_value_type):
    return field_value_type == Configuration.FieldValueType.JsonAlias \
        or field_value_type == Configuration.FieldValueType.Number \
        or field_value_type == Configuration.FieldValueType.String \
        or field_value_type == Configuration.FieldValueType.Bool \
        or field_value_type == Configuration.FieldValueType.Null


def __LogTwiceAddAnonymArgs(sheet_name: str, start_block_visible_number: int, end_block_visible_number: int,
                            applied_anonym_args_visible_number: int,
                            ignore_anonym_args_by_visible_number: dict[int, dict[str, str]]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Parameter', 'Description']
    pretty_table.align['Type'] = 'l'
    pretty_table.add_row(["Sheet name", sheet_name], divider=True)
    pretty_table.add_row(["Start block row number", start_block_visible_number], divider=True)
    pretty_table.add_row(["End block row number", end_block_visible_number], divider=True)
    pretty_table.add_row(["Applied anonym args from row number", applied_anonym_args_visible_number], divider=True)

    ignore_anonym_args_pretty_table = PrettyTable()
    ignore_anonym_args_pretty_table.field_names = ['Row number', 'Arg']
    for row_index, ignore_anonym_args in ignore_anonym_args_by_visible_number.items():
        ignore_anonym_args_pretty_table.add_row([row_index, ignore_anonym_args], divider=True)

    pretty_table.add_row(["Ignore anonym args", str(ignore_anonym_args_pretty_table)], divider=True)

    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Attempt added anonym args twice')}",
        "\n"
        f"{str(pretty_table)}"
    ]))
