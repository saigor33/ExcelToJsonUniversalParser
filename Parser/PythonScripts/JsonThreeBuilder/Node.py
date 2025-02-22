from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue


class Node:
    def __init__(self, field_name: str, node_value: BaseNodeValue, nodes):
        self.field_name = field_name
        self.node_value = node_value
        self.nodes = nodes
