from typing import Optional
from prettytable import PrettyTable
from RowToJsonConverter import AliasFuncStackLogFormatter
from RowToJsonConverter.Node import Node
from Tests import LogFormatter


class AliasFunc:
    def __init__(self, node: Node):
        self.__node = node

    def resolve(self, args: dict[str, str], root_field_names_stack: list[str], current_root_field_name: str) -> Node:
        missing_arg_name_by_path: dict[str, str] = {}
        field_names_stack: list[str] = []
        result_node = self._ResolveInternal(self.__node, args, missing_arg_name_by_path, field_names_stack)

        if bool(missing_arg_name_by_path):
            self._LogMissingArgs(missing_arg_name_by_path, root_field_names_stack, current_root_field_name)

        return result_node

    def _ResolveInternal(
            self,
            node: Node,
            args: dict[str, str],
            missing_arg_name_by_path: dict[str, str],
            field_names_stack: list[str]
    ) -> Node:
        value: str = self._TryResolveValue(node.value, args, missing_arg_name_by_path, field_names_stack, node.name)
        inner_nodes = None
        if node.inner_nodes is not None:
            inner_nodes = []
            for inner_node in node.inner_nodes:
                new_field_names_stack: list[str] = field_names_stack + [node.name]
                inner_nodes.append(
                    self._ResolveInternal(inner_node, args, missing_arg_name_by_path, new_field_names_stack))

        return Node(node.name, value, inner_nodes)

    @staticmethod
    def _TryResolveValue(
            value: str,
            args: dict[str, str],
            missing_arg_name_by_path: dict[str, str],
            field_names_stack: list[str],
            current_field_name: str
    ) -> Optional[str]:
        if value is None:
            return value
        elif value.startswith("%") and value.endswith("%"):
            arg_name = value[1:-1]
            if arg_name in args:
                return args[arg_name]
            else:
                field_name_stack = AliasFuncStackLogFormatter.stackFormat(field_names_stack, current_field_name)
                missing_arg_name_by_path[arg_name] = field_name_stack
                return arg_name
        else:
            return value

    def _LogMissingArgs(self, missing_arg_name_by_path: dict[str, str], root_field_names_stack: list[str],
                        current_root_field_name: str):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Alias func name', 'Feature fields stack', 'Missing arg']
        pretty_table.align['Alias func name'] = 'l'
        pretty_table.align['Feature fields stack'] = 'l'

        missing_args_pretty_table = PrettyTable()
        missing_args_pretty_table.field_names = ['Arg name', 'Fields stack']
        missing_args_pretty_table.align['Arg name'] = 'l'
        missing_args_pretty_table.align['Fields stack'] = 'l'

        for arg_name, fields_path in missing_arg_name_by_path.items():
            missing_args_pretty_table.add_row([LogFormatter.formatWarningColor(arg_name), fields_path], divider=True)

        alias_func_name = self.__node.name
        root_field_names_stack = AliasFuncStackLogFormatter.stackFormat(root_field_names_stack, current_root_field_name)
        pretty_table.add_row([alias_func_name, root_field_names_stack, str(missing_args_pretty_table)])

        print(''.join([
            f'\n\t{LogFormatter.formatWarning("Missing alias func args")}',
            f'\n\tDescription: Alias func args left unchanged',
            f'\n{str(pretty_table)}'
        ]))
