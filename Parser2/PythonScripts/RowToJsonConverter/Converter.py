import Configuration.FieldValueType
from prettytable import PrettyTable
import Configuration.ReferenceType
from typing import Optional
from RowToJsonConverter.Node import Node
from Sources.Row import Row
from Tests import LogFormatter


def convert(sheet_name: str, rows: list[Row]) -> list[Node]:
    result: list[Node] = []

    first_row_numbers_by_know_link_id: dict[str, int] = {}
    duplicate_link_id_row_numbers_by_link_id: dict[str, list[int]] = {}

    start_block_row_index: int = 0
    row_index = start_block_row_index
    last_row_index = len(rows) - 1
    while row_index <= last_row_index:
        node: Optional[Node] = None
        if row_index == last_row_index:
            node = _CreateNode(sheet_name, rows, start_block_row_index, last_row_index,
                               first_row_numbers_by_know_link_id, duplicate_link_id_row_numbers_by_link_id)
        elif rows[row_index + 1].link_id is not None:
            node = _CreateNode(sheet_name, rows, start_block_row_index, row_index,
                               first_row_numbers_by_know_link_id, duplicate_link_id_row_numbers_by_link_id)
            start_block_row_index = row_index + 1

        if node is not None:
            result.append(node)

        row_index += 1

    if bool(duplicate_link_id_row_numbers_by_link_id):
        _LogDuplicateLinKIds(sheet_name, first_row_numbers_by_know_link_id, duplicate_link_id_row_numbers_by_link_id)

    return result


def _CreateNode(
        sheet_name: str,
        rows,
        start_block_row_index,
        end_block_row_index,
        first_row_numbers_by_know_link_id: dict[str, int],
        duplicate_link_id_row_numbers_by_link_id: dict[str, list[int]]
) -> Optional[Node]:
    node_name = rows[start_block_row_index].link_id
    start_block_visible_number = rows[start_block_row_index].visible_number

    if node_name not in first_row_numbers_by_know_link_id:
        first_row_numbers_by_know_link_id[node_name] = start_block_visible_number
    else:
        if node_name not in duplicate_link_id_row_numbers_by_link_id:
            duplicate_link_id_row_numbers_by_link_id[node_name] = []
        duplicate_link_id_row_numbers_by_link_id[node_name].append(start_block_visible_number)
        return None

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
            # 0. Has only linkId. If next layer field is empty
            if not __IsEmptyLinkIdBlock(row):
                __LogEmptyTypeRow(sheet_name, row.visible_number, row)
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


def __IsEmptyLinkIdBlock(row: Row):
    return row.link_id is not None \
        and row.field_name is None \
        and row.field_value is None \
        and row.alias_func_arg_value is None \
        and row.anonym_args is None


def __LogEmptyTypeRow(sheet_name: str, row_visible_number: int, row: Row):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Parameter', 'Description']
    pretty_table.align['Parameter'] = 'l'
    pretty_table.add_row(["Sheet name", sheet_name], divider=True)
    pretty_table.add_row(["Row number", row_visible_number], divider=True)

    row_content_pretty_table = PrettyTable()
    row_content_pretty_table.field_names = ['Parameter', 'Value']
    row_content_pretty_table.align['Parameter'] = 'l'
    row_content_pretty_table.align['Value'] = 'l'
    row_content_pretty_table.add_row(["link_id", row.link_id], divider=False)
    row_content_pretty_table.add_row(["field_name", row.field_name], divider=False)
    highlight_field_value_type = LogFormatter.formatWarningColor(row.field_value_type)
    row_content_pretty_table.add_row(["field_value_type", highlight_field_value_type], divider=False)
    row_content_pretty_table.add_row(["field_value", row.field_value], divider=False)
    row_content_pretty_table.add_row(["alias_func_arg_value", row.alias_func_arg_value], divider=False)
    row_content_pretty_table.add_row(["anonym_args", row.anonym_args], divider=False)

    pretty_table.add_row(["Row content", str(row_content_pretty_table)], divider=True)

    print("".join([
        f"\n\t{LogFormatter.formatWarningColor('Warning. Missing value type')}",
        f"\n{str(pretty_table)}"
    ]))


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


def _LogDuplicateLinKIds(sheet_name: str, first_row_numbers_by_know_link_id: dict[str, int],
                         duplicate_link_id_row_numbers_by_link_id: dict[str, list[int]]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Sheet name', 'Duplicate link id']
    pretty_table.align['Sheet name'] = 'l'

    duplicate_link_ids_pretty_table = PrettyTable()
    duplicate_link_ids_pretty_table.field_names = ['id', 'Row numbers']
    duplicate_link_ids_pretty_table.align['Row numbers'] = 'r'

    for link_id, row_numbers in duplicate_link_id_row_numbers_by_link_id.items():
        highlight_link_id = LogFormatter.formatWarningColor(link_id)
        first_row_number = first_row_numbers_by_know_link_id[link_id]
        row_numbers_text = '\n'.join([str(first_row_number)] + [str(x) for x in row_numbers])
        duplicate_link_ids_pretty_table.add_row([highlight_link_id, row_numbers_text], divider=True)

    pretty_table.add_row([sheet_name, str(duplicate_link_ids_pretty_table)], divider=True)

    print(''.join([
        f'\n\t{LogFormatter.formatWarning("Duplicate link id")}',
        f'\n\tDescription: duplicate blocks with link id will be ignored',
        f'\n{str(pretty_table)}'
    ]))
