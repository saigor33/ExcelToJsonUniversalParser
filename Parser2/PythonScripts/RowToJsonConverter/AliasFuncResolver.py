from prettytable import PrettyTable
from Configuration import FieldValueType
from JsonAlias import Alias
from RowToJsonConverter import AliasFuncNodesJoiner, AliasFuncStackLogFormatter
from RowToJsonConverter.AliasFunc import AliasFunc
from RowToJsonConverter.Node import Node
from Tests import LogFormatter


class AliasFuncResolver:
    __alias_funcs_by_name: dict[str, AliasFunc]
    __json_aliases: dict[str, Alias]

    def __init__(self, alias_funcs_by_name: dict[str, AliasFunc], json_aliases: dict[str, Alias]):
        self.__alias_funcs_by_name = alias_funcs_by_name
        self.__json_aliases = json_aliases

    def resolve(self, feature_name: str, alias_func_name: str, alias_func_args: dict[str, str],
                alias_func_stack: list[str], root_field_names_stack: list[str], current_root_field_name: str) -> Node:
        if alias_func_name in alias_func_stack:
            self.__LogInfiniteLoopAliasFunc(feature_name, alias_func_name, alias_func_stack)
            return Node(alias_func_name, str(alias_func_args), [])

        if alias_func_name in self.__json_aliases:
            # todo: convert json text to Nodes
            json_alias: Alias = self.__json_aliases[alias_func_name]
            node_value = json_alias.resolve(
                alias_func_args,
                alias_func_stack,
                root_field_names_stack,
                current_root_field_name
            )
            inner_node = Node(FieldValueType.JsonAlias, node_value, None)
            return Node(None, None, [inner_node])
        elif alias_func_name in self.__alias_funcs_by_name:
            new_alias_func_stack: list[str] = alias_func_stack + [alias_func_name]
            alias_func: AliasFunc = self.__alias_funcs_by_name[alias_func_name]
            resolved_func_node = alias_func.resolve(alias_func_args, root_field_names_stack, current_root_field_name)
            return AliasFuncNodesJoiner.join(feature_name, resolved_func_node, self, new_alias_func_stack,
                                             root_field_names_stack, current_root_field_name)
        else:
            self.__LogMissingAliasFunc(feature_name, alias_func_name, alias_func_args)
            return Node(alias_func_name, str(alias_func_args), [])

    @staticmethod
    def __LogMissingAliasFunc(feature_name: str, alias_func_name: str, alias_func_args: dict[str, str]):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Parameter', 'Description']
        pretty_table.align['Parameter'] = 'l'
        pretty_table.align['Description'] = 'l'

        pretty_table.add_row(["Feature name", feature_name], divider=True)
        pretty_table.add_row(["Alias func name", LogFormatter.formatWarningColor(alias_func_name)], divider=True)
        pretty_table.add_row(["Alias func args", alias_func_args], divider=True)

        print(''.join([
            f'\n\t{LogFormatter.formatWarning("Missing alias func")}',
            f'\n{str(pretty_table)}'
        ]))

    @staticmethod
    def __LogInfiniteLoopAliasFunc(feature_name: str, alias_func_name: str, alias_func_stack: list[str]):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Parameter', 'Description']
        pretty_table.align['Parameter'] = 'l'
        pretty_table.align['Description'] = 'l'

        pretty_table.add_row(["Feature name", feature_name], divider=True)
        pretty_table.add_row(["Alias func name", LogFormatter.formatWarningColor(alias_func_name)], divider=True)
        stack_format = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, alias_func_name)
        pretty_table.add_row(["Alias func stack", stack_format], divider=True)
        print(''.join([
            f'\n\t{LogFormatter.formatWarning("Infinite alias funcs loop detected")}',
            f'\n{str(pretty_table)}'
        ]))
