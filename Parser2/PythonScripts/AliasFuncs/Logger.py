from typing import Optional
from prettytable import PrettyTable
from RowToJsonConverter import AliasFuncStackLogFormatter
from Tests import LogFormatter


def logInvalidArgs(
        missing_arg_name_by_path: Optional[dict[str, str]],
        unused_args: Optional[dict[str, str]],
        alias_func_stack: list[str],
        current_alias_func: str,
        formated_root_field_names_stack: list[str],
        current_root_field_name: str
):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Fields stack', 'Funcs stack', 'Invalid args']
    pretty_table.align['Fields stack'] = 'l'
    pretty_table.align['Funcs stack'] = 'l'

    invalid_args_pretty_table = PrettyTable()
    invalid_args_pretty_table.field_names = ['Type', 'Description']
    invalid_args_pretty_table.align['Description'] = 'l'

    if bool(missing_arg_name_by_path):
        invalid_args_pretty_table.add_row(
            ['Missing args', _GenerateMissingArgsLog(missing_arg_name_by_path)], divider=True)
    if bool(unused_args):
        invalid_args_pretty_table.add_row(['Unused args', _GenerateUnusedArgsLog(unused_args)], divider=True)

    formated_root_field_names_stack = \
        AliasFuncStackLogFormatter.stackFormat(formated_root_field_names_stack, current_root_field_name)
    formated_alias_func_stack = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, current_alias_func)
    pretty_table.add_row(
        [
            formated_root_field_names_stack,
            formated_alias_func_stack,
            str(invalid_args_pretty_table)
        ],
        divider=True)

    print("".join([
        f"\n\t{LogFormatter.formatWarning('Invalid json alias func args detect')}"
        f"\n{str(pretty_table)}"
    ]))


def _GenerateMissingArgsLog(missing_arg_name_by_path: dict[str, str]) -> PrettyTable:
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Arg name', 'AliasFunc fields stack']
    pretty_table.align['Arg name'] = 'l'
    pretty_table.align['AliasFunc fields stack'] = 'l'

    for fields_path, arg_name in missing_arg_name_by_path.items():
        pretty_table.add_row([LogFormatter.formatWarningColor(arg_name), fields_path], divider=True)

    return pretty_table


def _GenerateUnusedArgsLog(unused_args: dict[str, str]) -> PrettyTable:
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Arg name', 'Arg value']
    pretty_table.align = 'l'

    for arg_name, arg_value in unused_args.items():
        pretty_table.add_row([LogFormatter.formatWarningColor(arg_name), arg_value], divider=True)

    return pretty_table
