from typing import Optional
from RowToJsonConverter.Node import Node


class AliasFunc:
    def __init__(self, node: Node):
        self.__node = node

    def resolve(self, args: dict[str, str]) -> Node:
        return self._ResolveInternal(self.__node, args)

    def _ResolveInternal(self, node: Node, args: dict[str, str]) -> Node:
        value: str = self._TryResolveValue(node.value, args)
        inner_nodes = None
        if node.inner_nodes is not None:
            inner_nodes = []
            for inner_node in node.inner_nodes:
                inner_nodes.append(self._ResolveInternal(inner_node, args))

        return Node(node.name, value, inner_nodes)

    @staticmethod
    def _TryResolveValue(value: str, args: dict[str, str]) -> Optional[str]:
        if value is None:
            return value
        elif value.startswith("%") and value.endswith("%"):
            arg_name = value[1:-1]
            if arg_name in args:
                return args[arg_name]
            else:
                # todo: use table output
                print(f"arg_name not found {arg_name}")
                return arg_name
        else:
            return value
