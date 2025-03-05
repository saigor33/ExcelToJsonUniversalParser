from typing import Optional

from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer


def build(ordered_by_level_sheet_names: list[str], nodes_by_sheet_name: dict[str, list[Node]]) -> NodesLayer:
    result: Optional[NodesLayer] = None
    for sheet_name in reversed(ordered_by_level_sheet_names):
        result = NodesLayer(sheet_name, nodes_by_sheet_name[sheet_name], result)

    return result
