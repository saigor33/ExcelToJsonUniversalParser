from typing import Optional
from AliasFuncs import Logger
from RowToJsonConverter import AliasFuncStackLogFormatter
from RowToJsonConverter.Node import Node


class AliasFunc:
    def __init__(self, node: Node):
        self.__node = node

    def resolve(self, args: dict[str, str], alias_func_stack: list[str], root_field_names_stack: list[str],
                current_root_field_name: str) -> Node:
        used_arg_names: set[str] = set()
        missing_arg_name_by_path: dict[str, str] = {}
        field_names_stack: list[str] = []
        result_node = self._ResolveInternal(self.__node, args, missing_arg_name_by_path, field_names_stack,
                                            used_arg_names)

        unused_args: dict[str, str] = {k: v for k, v in args.items() if k not in used_arg_names}
        if bool(missing_arg_name_by_path) or bool(unused_args):
            current_alais_func = self.__node.name
            Logger.logInvalidArgs(
                missing_arg_name_by_path,
                unused_args,
                alias_func_stack,
                current_alais_func,
                root_field_names_stack,
                current_root_field_name
            )

        return result_node

    def _ResolveInternal(
            self,
            node: Node,
            args: dict[str, str],
            missing_arg_name_by_path: dict[str, str],
            field_names_stack: list[str],
            used_arg_names: set[str]
    ) -> Node:
        value: str = self._TryResolveValue(node.value, args, missing_arg_name_by_path, field_names_stack, node.name,
                                           used_arg_names)
        inner_nodes = None
        if node.inner_nodes is not None:
            inner_nodes = []
            for inner_node in node.inner_nodes:
                new_field_names_stack: list[str] = field_names_stack + [node.name]
                inner_nodes.append(
                    self._ResolveInternal(inner_node, args, missing_arg_name_by_path, new_field_names_stack,
                                          used_arg_names))

        return Node(node.name, value, inner_nodes)

    @staticmethod
    def _TryResolveValue(
            value: str,
            args: dict[str, str],
            missing_arg_name_by_path: dict[str, str],
            field_names_stack: list[str],
            current_field_name: str,
            used_arg_names: set[str]
    ) -> Optional[str]:
        if value is None:
            return value
        elif value.startswith("%") and value.endswith("%"):
            arg_name = value[1:-1]
            if arg_name in args:
                used_arg_names.add(arg_name)
                return args[arg_name]
            else:
                field_name_stack = AliasFuncStackLogFormatter.stackFormat(field_names_stack, current_field_name)
                missing_arg_name_by_path[arg_name] = field_name_stack
                return arg_name
        else:
            return value
