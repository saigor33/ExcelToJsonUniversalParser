from __future__ import annotations

from typing import Optional

from RowToJsonConverter.Node import Node


class NodesLayer:
    def __init__(self, sheet_name: str, nodes: list[Node], next_nodes_layer: Optional[NodesLayer]):
        self.sheet_name = sheet_name
        self.nodes = nodes
        self.next_nodes_layer = next_nodes_layer

