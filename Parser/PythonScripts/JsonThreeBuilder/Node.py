from __future__ import annotations

from typing import Optional

from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue


class Node:
    field_name: str
    node_value: BaseNodeValue
    nodes: list[Node]

    def __init__(self, field_name: str, node_value: BaseNodeValue, nodes: Optional[list[Node]]):
        self.field_name = field_name
        self.node_value = node_value
        self.nodes = nodes
