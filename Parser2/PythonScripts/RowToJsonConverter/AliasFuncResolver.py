from RowToJsonConverter import AliasFuncNodesJoiner
from RowToJsonConverter.AliasFunc import AliasFunc
from RowToJsonConverter.Node import Node


class AliasFuncResolver:
    def __init__(self, nodes_by_alias_func_signature: dict[str, Node]):
        alias_funcs_by_name: dict[str, AliasFunc] = {}
        for alias_func_signature, node in nodes_by_alias_func_signature.items():
            alias_funcs_by_name[alias_func_signature] = AliasFunc(node)

        self.__alias_funcs_by_name = alias_funcs_by_name

    def resolve(self, feature_name: str, alias_func_name: str, alias_func_args: dict[str, str],
                alias_func_stack: list[str]) -> Node:
        if alias_func_name in alias_func_stack:
            # todo: format print
            print(f"Infinite loop detected stack={alias_func_stack}, current_alias_func={alias_func_name}")
            return Node(alias_func_name, str(alias_func_args), [])

        if alias_func_name not in self.__alias_funcs_by_name:
            print(f"Alias func not found '{alias_func_name}', args={alias_func_args}")
            return Node(alias_func_name, str(alias_func_args), [])

        new_alias_func_stack = alias_func_stack + [alias_func_name]
        resolved_func_node = self.__alias_funcs_by_name[alias_func_name].resolve(alias_func_args)
        return AliasFuncNodesJoiner.join(feature_name, resolved_func_node, self, new_alias_func_stack)
