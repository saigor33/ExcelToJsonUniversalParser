from __future__ import annotations

from typing import Optional


class Node:
    def __init__(self, name: str, value: str, inner_nodes: Optional[list[Node]] = None):
        self.name = name
        self.value = value
        self.inner_nodes = inner_nodes
