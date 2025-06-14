from typing import Optional
from RowToJsonConverter import AliasFuncStackLogFormatter
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.Node import Node
from prettytable import PrettyTable
import Configuration.ReferenceType
from Tests import LogFormatter


def join(
        feature_name: str,
        node: Node,
        alias_func_resolver: AliasFuncResolver,
        alias_func_stack: list[str],
        root_field_names_stack: list[str],
        current_root_field_name: str
) -> Node:
    return _JoinInternal(feature_name, node, alias_func_resolver, alias_func_stack, root_field_names_stack,
                         current_root_field_name)


def _JoinInternal(
        feature_name: str,
        node: Node,
        alias_func_resolver: AliasFuncResolver,
        alias_func_stack: list[str],
        root_field_names_stack: list[str],
        current_root_field_name: str
) -> Node:
    if node.value == Configuration.ReferenceType.AliasFunc:
        if node.inner_nodes is None:
            raise Exception(f"AliasFunc node: inner_nodes can't be None. node.name={node.name}")
        if len(node.inner_nodes) != 1:
            raise Exception(f"AliasFunc node: inner_nodes should be count equal to 1. node.name={node.name}")

        func_node: Node = node.inner_nodes[0]
        alias_func_name = func_node.name
        if func_node.inner_nodes is None:
            raise Exception(
                f"AliasFunc node: args nodes can't be None",
                f"node.name={node.name}",
                f"alias_func_name={alias_func_name}"
            )

        alias_func_args = GetAliasFuncArgs(alias_func_name, alias_func_stack, feature_name, func_node, node)

        resolved_alias_func_node = \
            alias_func_resolver.resolve(feature_name, alias_func_name, alias_func_args, alias_func_stack,
                                        root_field_names_stack, current_root_field_name)
        return Node(node.name, resolved_alias_func_node.value, resolved_alias_func_node.inner_nodes)
    elif node.inner_nodes is not None:
        for index, inner_node in enumerate(node.inner_nodes):
            new_root_field_names_stack = root_field_names_stack + [current_root_field_name]
            new_current_root_field_name = inner_node.name  # todo: can be Configuration.ReferenceType.AliasFunc
            node.inner_nodes[index] = \
                _JoinInternal(feature_name, inner_node, alias_func_resolver, alias_func_stack,
                              new_root_field_names_stack, new_current_root_field_name)
        return node
    else:
        return node


def GetAliasFuncArgs(alias_func_name, alias_func_stack, feature_name, func_node, node):
    alias_func_args: dict[str, str] = {}
    duplicate_alias_func_arg_names: Optional[set[str]] = None
    for arg_node in func_node.inner_nodes:
        arg_name = arg_node.name
        if arg_name in alias_func_args:
            if duplicate_alias_func_arg_names is None:
                duplicate_alias_func_arg_names = set[str]()
            duplicate_alias_func_arg_names.add(arg_name)
        else:
            alias_func_args[arg_name] = arg_node.value

    if duplicate_alias_func_arg_names is not None:
        _LogDuplicateAliasFuncArgNames(feature_name, node.name, alias_func_stack, alias_func_name,
                                       duplicate_alias_func_arg_names)
    return alias_func_args


def _LogDuplicateAliasFuncArgNames(
        feature_name: str,
        field_name: str,
        alias_func_stack: list[str],
        alias_func_name: str,
        duplicate_alias_func_arg_names: set[str]
) -> None:
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Feature name', 'Field name', 'Alias func stack', 'duplicate args']
    pretty_table.align['Alias func stack'] = 'l'

    highlight_duplicate_args = '\n'.join([LogFormatter.formatWarningColor(x) for x in duplicate_alias_func_arg_names])
    formated_alias_stack = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, alias_func_name)
    pretty_table.add_row([feature_name, field_name, formated_alias_stack, highlight_duplicate_args])

    print("".join([
        f"\t{LogFormatter.formatWarningColor('Warning: duplicate alias func arg name.')}\n",
        str(pretty_table)
    ]))
