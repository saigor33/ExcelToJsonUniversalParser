from typing import Optional
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.Node import Node
from colorama import Fore, Style
from prettytable import PrettyTable
import Configuration.ReferenceType


def join(
        feature_name: str,
        node: Node,
        alias_func_resolver: AliasFuncResolver,
        alias_func_stack: list[str]
) -> Node:
    return _JoinInternal(feature_name, node, alias_func_resolver, alias_func_stack)


def _JoinInternal(
        feature_name: str,
        node: Node,
        alias_func_resolver: AliasFuncResolver,
        alias_func_stack: list[str]
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

        resolved_alias_func_node = alias_func_resolver.resolve(feature_name, alias_func_name, alias_func_args,
                                                               alias_func_stack)
        return Node(node.name, resolved_alias_func_node.value, resolved_alias_func_node.inner_nodes)
    elif node.inner_nodes is not None:
        for index, inner_node in enumerate(node.inner_nodes):
            node.inner_nodes[index] = _JoinInternal(feature_name, inner_node, alias_func_resolver, alias_func_stack)
        return node
    else:
        return node


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

    args_separator = f'{Style.RESET_ALL}\n{Fore.YELLOW}'
    formated_duplicate_alias_func_arg_names = args_separator.join(duplicate_alias_func_arg_names)
    highlight_duplicate_args = f"{Fore.YELLOW}{formated_duplicate_alias_func_arg_names}{Style.RESET_ALL}"
    formated_alias_stack = _FormatAliasFuncStack(alias_func_stack, alias_func_name)
    pretty_table.add_row([feature_name, field_name, formated_alias_stack, highlight_duplicate_args])

    print("".join([
        f"\t{Fore.YELLOW}Warning: duplicate alias func arg name.{Style.RESET_ALL}\n",
        str(pretty_table)
    ]))


def _FormatAliasFuncStack(alias_func_stack: list[str], alias_func_name: str) -> str:
    log = \
        [
            f"->{alias_func_name}",
            "\n".join(reversed(alias_func_stack)) if len(alias_func_stack) > 0 else "<start>",
        ]
    return "\n".join(log)
