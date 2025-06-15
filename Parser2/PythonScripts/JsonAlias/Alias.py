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

    def resolve(
            self,
            alias_func_args: dict[str, str],
            alias_func_stack: list[str],
            root_field_names_stack: list[str],
            current_root_field_name: str
    ) -> str:
        used_arg_names: set[str] = set()
        unused_arg_names: Optional[set[str]] = None
        missing_arg_names: Optional[set[str]] = None

        texts: list[str] = []
        for item in self.items:
            item_type = type(item)
            if item_type == ArgItem:
                arg_item: ArgItem = item
                if arg_item.arg_name in alias_func_args:
                    used_arg_names.add(arg_item.arg_name)
                    texts.append(alias_func_args[arg_item.arg_name])
                else:
                    if missing_arg_names is None:
                        missing_arg_names = set()
                    missing_arg_names.add(arg_item.arg_name)
            elif item_type == TextItem:
                text_item: TextItem = item
                texts.append(text_item.text)
            else:
                raise Exception("Unknown item type", item_type, item)

        for arg_name, arg_value in alias_func_args.items():
            if arg_name not in used_arg_names:
                if unused_arg_names is None:
                    unused_arg_names = set()
                unused_arg_names.add(arg_name)

        if missing_arg_names is not None or unused_arg_names is not None:
            self.__LogInvalidArgs(missing_arg_names, unused_arg_names, alias_func_stack, root_field_names_stack,
                                  current_root_field_name)

        join = ''.join(texts)
        return join.replace('\'', '"')

    def __LogInvalidArgs(
            self,
            missing_arg_names: Optional[set[str]],
            unused_arg_names: Optional[set[str]],
            alias_func_stack: list[str],
            root_field_names_stack: list[str],
            current_root_field_name: str
    ):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Fields stack', 'Funcs stack', 'Invalid args']
        pretty_table.align['Fields stack'] = 'l'
        pretty_table.align['Funcs stack'] = 'l'
        invalid_types_pretty_table = Alias.__FormatInvalidArgs(missing_arg_names, unused_arg_names)

        root_field_names_stack = AliasFuncStackLogFormatter.stackFormat(root_field_names_stack, current_root_field_name)
        formated_alias_func_stack = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, self.name)
        pretty_table.add_row([root_field_names_stack, formated_alias_func_stack, str(invalid_types_pretty_table)],
                             divider=True)

        print("".join([
            f"\n\t{LogFormatter.formatWarning('Invalid json alias func args detect')}"
            f"\n{str(pretty_table)}"
        ]))

    @staticmethod
    def __FormatInvalidArgs(missing_arg_names: Optional[set[str]], unused_arg_names: Optional[set[str]]):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Type', 'Name']
        pretty_table.align['Type'] = 'l'
        if missing_arg_names is not None:
            highlight_missing_arg_names = '\n'.join([LogFormatter.formatWarningColor(x) for x in missing_arg_names])
            pretty_table.add_row(['Missing args', highlight_missing_arg_names], divider=True)
        if unused_arg_names is not None:
            highlight_unused_arg_names = '\n'.join([LogFormatter.formatWarningColor(x) for x in unused_arg_names])
            pretty_table.add_row(['Unused args', highlight_unused_arg_names], divider=True)
        return pretty_table
