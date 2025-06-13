from typing import Optional
from prettytable import PrettyTable
from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer
from Tests import LogFormatter


def build(ordered_by_level_sheet_names: list[str], nodes_by_sheet_name: dict[str, list[Node]]) -> NodesLayer:
    result: Optional[NodesLayer] = None

    missing_sheet_names: Optional[list[str]] = None
    for sheet_name in reversed(ordered_by_level_sheet_names):
        if sheet_name in nodes_by_sheet_name:
            result = NodesLayer(sheet_name, nodes_by_sheet_name[sheet_name], result)
        else:
            if missing_sheet_names is None:
                missing_sheet_names = []
            missing_sheet_names.append(sheet_name)

    if bool(missing_sheet_names):
        _LogSheetNamesNotFound(missing_sheet_names)

    return result


def _LogSheetNamesNotFound(missing_sheet_names: list[str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Sheet name']
    pretty_table.align['Sheet name'] = 'l'

    highlight_missing_sheet_names = '\n'.join([LogFormatter.formatErrorColor(x) for x in missing_sheet_names])
    pretty_table.add_row([highlight_missing_sheet_names])

    print(''.join([
        f'\n\t{LogFormatter.formatError("Missing nodes layer excel sheet")}',
        f'\n{str(pretty_table)}'
    ]))
