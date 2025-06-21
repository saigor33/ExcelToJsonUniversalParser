from typing import Optional
from prettytable import PrettyTable
from JsonAlias.Alias import Alias, Item, TextItem, ArgItem
from Tests import LogFormatter


class Pattern:
    def __init__(self, open_part: str, close_part: str):
        self.open_part = open_part
        self.close_part = close_part


def create(name: str, json_alias_func_text: str) -> Alias:
    items: list[Item] = __Create(name, json_alias_func_text)

    return Alias(name, items)


def __Create(name: str, text: str) -> list[Item]:
    result: [Item] = []

    invalid_arg_warnings: list[PrettyTable] = []

    # %arg%
    # "%arg%"
    # \"%arg%\"

    patterns: list[Pattern] = [
        Pattern(open_part='\"%', close_part='%\"'),
        Pattern(open_part='\'%', close_part='%\''),
        Pattern(open_part='%', close_part='%')
    ]

    text_len = len(text)
    substring_start_index: int = 0

    char_index: int = 0
    while char_index < text_len:
        current_pattern: Optional[Pattern] = None
        for pattern in patterns:
            if __IsStartPattern(char_index, text, pattern.open_part):
                current_pattern = pattern

        if current_pattern is not None:
            arg_name_start_index = char_index + len(current_pattern.close_part)

            first_close_pattern, first_close_pattern_start_char_index = \
                __FindFirstClosePartPatter(text, arg_name_start_index, patterns, current_pattern)

            if first_close_pattern is not None and first_close_pattern == current_pattern:
                result.append(TextItem(text[substring_start_index:char_index]))

                arg_with_type_text = text[arg_name_start_index: first_close_pattern_start_char_index]
                result.append(_CreateArgItem(arg_with_type_text, invalid_arg_warnings))

                substring_start_index = first_close_pattern_start_char_index + len(current_pattern.close_part)
                char_index = substring_start_index
            else:
                char_index += 1
        else:
            char_index += 1

    if substring_start_index < text_len:
        result.append(TextItem(text[substring_start_index:]))

    if bool(invalid_arg_warnings):
        _LogInvalidValue(name, invalid_arg_warnings)

    return result


def __FindFirstClosePartPatter(text: str, start_index: int, patterns: list[Pattern], current_pattern: Pattern):
    index: int = start_index
    while index < len(text):
        if __IsStartPattern(index, text, current_pattern.close_part):
            return current_pattern, index
        for pattern in patterns:
            if pattern != current_pattern and __IsStartPattern(index, text, pattern.close_part):
                return pattern, index
        index += 1

    return None, None


def __IsStartPattern(char_index: int, text: str, open_patter: str) -> bool:
    for open_pattern_char_index in range(len(open_patter)):
        if text[char_index + open_pattern_char_index] != open_patter[open_pattern_char_index]:
            return False

    return True


def _CreateArgItem(arg_with_type_text: str, warnings: list[PrettyTable]) -> ArgItem:
    split_arg = arg_with_type_text.split(':')

    if len(split_arg) != 2:
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Description', 'Arg']
        pretty_table.align = 'l'
        pretty_table.add_row(["Type is not specified", LogFormatter.formatWarningColor(arg_with_type_text)])
        warnings.append(pretty_table)

        return ArgItem(arg_with_type_text, ArgItem.ValueType.String)

    arg_name = split_arg[0]
    arg_type = split_arg[1]

    is_type_valid = \
        arg_type == ArgItem.ValueType.Bool \
        or arg_type == ArgItem.ValueType.String \
        or arg_type == ArgItem.ValueType.Number

    if not is_type_valid:
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Description', 'Arg name', 'Arg type']
        pretty_table.align = 'l'
        pretty_table.add_row(["Unknown arg type", arg_name, LogFormatter.formatWarningColor(arg_type)])
        warnings.append(pretty_table)
        return ArgItem(arg_with_type_text, ArgItem.ValueType.String)

    return ArgItem(arg_name, arg_type)


def _LogInvalidValue(
        alias_func_name,
        invalid_arg_warnings: list[PrettyTable]
):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Alias func name', 'Warnings']

    pretty_table.add_row([alias_func_name, '\n\n'.join([str(x) for x in invalid_arg_warnings])])

    print(''.join([
        f'\n\t{LogFormatter.formatWarning("Invalid json alias func arg")}',
        f'\n{str(pretty_table)}'
    ]))
