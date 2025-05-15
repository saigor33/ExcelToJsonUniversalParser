from Configuration import FieldValueType
from JsonAlias import Alias
from RowToJsonConverter import AliasFuncNodesJoiner
from RowToJsonConverter.AliasFunc import AliasFunc
from RowToJsonConverter.Node import Node


class AliasFuncResolver:
    __alias_funcs_by_name: dict[str, AliasFunc]
    __json_aliases: dict[str, Alias]

    def __init__(self, alias_funcs_by_name: dict[str, AliasFunc], json_aliases: dict[str, Alias]):
        self.__alias_funcs_by_name = alias_funcs_by_name
        self.__json_aliases = json_aliases

    def resolve(self, feature_name: str, alias_func_name: str, alias_func_args: dict[str, str],
                alias_func_stack: list[str]) -> Node:
        if alias_func_name in alias_func_stack:
            # todo: format print
            print(f"Infinite loop detected stack={alias_func_stack}, current_alias_func={alias_func_name}")
            return Node(alias_func_name, str(alias_func_args), [])

        if alias_func_name in self.__json_aliases:
            # todo: convert json text to Nodes
            json_alias: Alias = self.__json_aliases[alias_func_name]
            node_value = json_alias.resolve(alias_func_args, alias_func_stack)
            inner_node = Node(FieldValueType.JsonAlias, node_value, None)
            return Node(None, None, [inner_node])
        elif alias_func_name in self.__alias_funcs_by_name:
            new_alias_func_stack: list[str] = alias_func_stack + [alias_func_name]
            resolved_func_node = self.__alias_funcs_by_name[alias_func_name].resolve(alias_func_args)
            return AliasFuncNodesJoiner.join(feature_name, resolved_func_node, self, new_alias_func_stack)
        else:
            print(f"Alias func not found '{alias_func_name}', args={alias_func_args}")
            return Node(alias_func_name, str(alias_func_args), [])
