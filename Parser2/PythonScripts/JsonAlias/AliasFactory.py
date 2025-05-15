from typing import Optional
from JsonAlias.Alias import Alias, Item, TextItem, ArgItem


class Pattern:
    def __init__(self, open_part: str, close_part: str):
        self.open_part = open_part
        self.close_part = close_part


def create(name: str, json_alias_func_text: str) -> Alias:
    items: list[Item] = __Create(json_alias_func_text)

    return Alias(name, items)


def __Create(text: str) -> list[Item]:
    result: [Item] = []

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
                result.append(ArgItem(text[arg_name_start_index: first_close_pattern_start_char_index]))

                substring_start_index = first_close_pattern_start_char_index + len(current_pattern.close_part)
                char_index = substring_start_index
            else:
                char_index += 1
        else:
            char_index += 1

    if substring_start_index < text_len:
        result.append(TextItem(text[substring_start_index:]))

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
