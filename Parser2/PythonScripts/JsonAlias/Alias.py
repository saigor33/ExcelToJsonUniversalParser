from RowToJsonConverter import AliasFuncStackLogFormatter
from Tests import LogFormatter
from typing import Optional
from prettytable import PrettyTable


class Item:
    pass


class TextItem(Item):
    def __init__(self, text: str):
        self.text = text


class ArgItem(Item):
    def __init__(self, arg_name: str):
        self.arg_name = arg_name


class Alias:
    def __init__(self, name: str, items: list[Item]):
        self.name = name
        self.items = items

    def resolve(self, alias_func_args: dict[str, str], alias_func_stack: list[str]):
        unknown_arg_names = None
        missing_arg_names = None

        texts: list[str] = []
        for item in self.items:
            item_type = type(item)
            if item_type == ArgItem:
                arg_item: ArgItem = item
                if arg_item.arg_name in alias_func_args:
                    texts.append(alias_func_args[arg_item.arg_name])
                else:
                    if unknown_arg_names is None:
                        unknown_arg_names = set()
                    unknown_arg_names.add(arg_item.arg_name)
            elif item_type == TextItem:
                text_item: TextItem = item
                texts.append(text_item.text)
            else:
                raise Exception("Unknown item type", item_type, item)

        if unknown_arg_names is not None or missing_arg_names is not None:
            self.__LogInvalidArgs(unknown_arg_names, missing_arg_names, alias_func_stack)

        join = ''.join(texts)
        return join.replace('\'', '"')

    def __LogInvalidArgs(self, unknown_arg_names: Optional[set[str]], missing_arg_names: Optional[set[str]],
                         alias_func_stack: list[str]):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Invalid args', 'Funcs stack']
        pretty_table.align['Funcs stack'] = 'l'
        invalid_types_pretty_table = Alias.__FormatInvalidArgs(missing_arg_names, unknown_arg_names)

        formated_alias_func_stack = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, self.name)
        pretty_table.add_row([str(invalid_types_pretty_table), formated_alias_func_stack], divider=True)

        print("".join([
            "\t"
            f"{LogFormatter.formatWarningColor('Warning. Invalid json alias func args detect.')}",
            "\n"
            f"{str(pretty_table)}"
        ]))

    @staticmethod
    def __FormatInvalidArgs(missing_arg_names, unknown_arg_names):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Type', 'Name']
        pretty_table.align['Type'] = 'l'
        if unknown_arg_names is not None:
            pretty_table.add_row(['Unknown', '\n'.join(unknown_arg_names)], divider=True)
            pass
        if missing_arg_names is not None:
            pretty_table.add_row(['Missing', '\n'.join(missing_arg_names)], divider=True)
            pass
        return pretty_table
