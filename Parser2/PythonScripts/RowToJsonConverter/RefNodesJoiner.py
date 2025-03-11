from colorama import Fore, Style
from prettytable import PrettyTable

import Configuration.ReferenceType
from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer


class RefNodesJoiner:

    def join(self, node: Node, nodes_layer: NodesLayer) -> Node:
        return self._JoinInternal(node, nodes_layer)

    def _JoinInternal(self, node: Node, nodes_layer: NodesLayer):
        if node.inner_nodes is None:
            # it is not ref node. Ref node has inner
            pass
        elif self._IsRefNode(node):
            node.inner_nodes = self._GetRefValue(node, nodes_layer)
        else:
            for index, inner_node in enumerate(node.inner_nodes):
                if inner_node.inner_nodes is None:
                    # it is not ref node. Ref node has inner
                    pass
                elif self._IsRefNode(inner_node):
                    inner_node.inner_nodes = self._GetRefValue(inner_node, nodes_layer)
                else:
                    self._JoinInternal(inner_node, nodes_layer)

        return node

    @staticmethod
    def _IsRefNode(node) -> bool:
        if node is None:
            raise Exception("Node can't be None")

        if len(node.inner_nodes) != 1:
            return False

        return node.inner_nodes[0].name == Configuration.ReferenceType.Ref

    def _GetRefValue(self, node: Node, nodes_layer: NodesLayer) -> list[Node]:
        if not self._IsRefNode(node):
            raise Exception("Node is no reference node")
        if nodes_layer is None:
            raise Exception("NodesLayer can't be NoNE")

        ref_node_field_name = node.inner_nodes[0].value

        for next_layer_node in nodes_layer.nodes:
            if next_layer_node.name == ref_node_field_name:
                for index, next_layer_inner_node in enumerate(next_layer_node.inner_nodes):
                    next_layer_node.inner_nodes[index] = self._JoinInternal(next_layer_inner_node,
                                                                            nodes_layer.next_nodes_layer)
                return next_layer_node.inner_nodes

        print(Fore.RED + 'Error: Missing ref value' + Style.RESET_ALL)

        table = PrettyTable()
        table.field_names = ["Search sheet name", "id"]
        highlighted_ref_node_field_name = Fore.RED + ref_node_field_name + Style.RESET_ALL
        table.add_row([nodes_layer.sheet_name, highlighted_ref_node_field_name])
        error: list[str] = [
            '\n\tDescription: Unknown "id"',
            '\n' + str(table),
            '\n'
        ]
        print("".join(error))
        return []
