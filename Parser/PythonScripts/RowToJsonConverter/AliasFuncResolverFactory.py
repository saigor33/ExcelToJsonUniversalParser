from prettytable import PrettyTable
from JsonAlias import Alias
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.AliasFunc import AliasFunc
from RowToJsonConverter.Node import Node
from Tests import LogFormatter


def create(nodes_by_alias_func_signature: dict[str, Node], json_aliases: dict[str, Alias]) -> AliasFuncResolver:
    duplicate_alias_func_names: list[str] = []

    alias_funcs_by_name: dict[str, AliasFunc] = {}
    for alias_func_signature, node in nodes_by_alias_func_signature.items():
        if alias_func_signature in json_aliases:
            duplicate_alias_func_names.append(alias_func_signature)
        else:
            alias_funcs_by_name[alias_func_signature] = AliasFunc(node)

    if bool(duplicate_alias_func_names):
        __LogDuplicateAliasFuncs(duplicate_alias_func_names)

    return AliasFuncResolver(alias_funcs_by_name, json_aliases)


def __LogDuplicateAliasFuncs(alias_func_names: list[str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Alias func name']
    pretty_table.align['Alias func name'] = 'l'
    for alias_func_name in alias_func_names:
        pretty_table.add_row([alias_func_name], divider=True)
    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Duplicate alias func name between json and table alias funcs.')}",
        "\n\t"
        "Will be used json alias func."
        "\n"
        f"{str(pretty_table)}"
    ]))
