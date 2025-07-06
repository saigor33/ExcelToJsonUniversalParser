from prettytable import PrettyTable
from AliasFuncs import Logger
from typing import Optional
from RowToJsonConverter import AliasFuncStackLogFormatter
from Tests import LogFormatter


class Item:
    pass


class TextItem(Item):
    def __init__(self, text: str):
        self.text = text


class ArgItem(Item):
    class ValueType:
        String = 'str'
        Number = 'num'
        Bool = 'bool'
        # Null can be set in alias func jsom.

    def __init__(self, arg_name: str, arg_type: str):
        self.arg_name = arg_name
        self._arg_type = arg_type

    def convertValue(
            self,
            arg_value: str,
            alias_func_stack: list[str],
            current_alias_func_name: str,
            root_field_names_stack: list[str],
            current_root_field_name: str
    ) -> str:
        if self._arg_type == ArgItem.ValueType.String:
            return arg_value
        elif self._arg_type == ArgItem.ValueType.Number:
            return arg_value
        elif self._arg_type == ArgItem.ValueType.Bool:
            bool_value = arg_value.lower()
            if bool_value == 'true' or bool_value == '1' or bool_value == '1.0':
                return "true"
            if bool_value == 'false' or bool_value == '0' or bool_value == '0.0':
                return "false"

            self._LogInvalidValue(
                arg_value,
                alias_func_stack,
                current_alias_func_name,
                root_field_names_stack,
                current_root_field_name
            )
            return arg_value
        else:
            raise Exception(f'Unsupported arg type for json alias func. (arg_type:{self._arg_type})')

    def _LogInvalidValue(
            self,
            arg_value: str,
            alias_func_stack: list[str],
            current_alias_func_name: str,
            root_field_names_stack: list[str],
            current_root_field_name: str
    ):
        pretty_table = PrettyTable()
        pretty_table.field_names = ['Fields stack', 'Funcs stack', 'Arg name', 'Arg target type', 'Arg value']
        pretty_table.align = 'l'

        formated_root_field_names_stack = \
            AliasFuncStackLogFormatter.stackFormat(root_field_names_stack, current_root_field_name)
        formated_alias_func_stack = AliasFuncStackLogFormatter.stackFormat(alias_func_stack, current_alias_func_name)
        pretty_table.add_row(
            [
                formated_root_field_names_stack,
                formated_alias_func_stack,
                self.arg_name,
                self._arg_type,
                LogFormatter.formatWarningColor(arg_value)
            ]
        )

        print(''.join([
            f'\n\t{LogFormatter.formatWarning("Invalid json alias func arg value")}',
            f'\n{str(pretty_table)}'
        ]))


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
        missing_arg_names_by_path: Optional[dict[str, str]] = None

        texts: list[str] = []
        for i, item in enumerate(self.items):
            item_type = type(item)
            if item_type == ArgItem:
                arg_item: ArgItem = item
                if arg_item.arg_name in alias_func_args:
                    used_arg_names.add(arg_item.arg_name)
                    arg_value_text = alias_func_args[arg_item.arg_name]
                    converted_art_value = arg_item.convertValue(
                        arg_value_text,
                        alias_func_stack,
                        self.name,
                        root_field_names_stack,
                        current_root_field_name
                    )
                    texts.append(converted_art_value)
                else:
                    if missing_arg_names_by_path is None:
                        missing_arg_names_by_path = {}
                    missing_arg_names_by_path[f'<unknown_stack_{i}>'] = arg_item.arg_name
            elif item_type == TextItem:
                text_item: TextItem = item
                texts.append(text_item.text)
            else:
                raise Exception("Unknown item type", item_type, item)

        unused_arg_names: dict[str, str] = {k: v for k, v in alias_func_args.items() if k not in used_arg_names}
        if bool(missing_arg_names_by_path) or bool(unused_arg_names):
            current_alias_func = self.name
            Logger.logInvalidArgs(
                missing_arg_names_by_path,
                unused_arg_names,
                alias_func_stack,
                current_alias_func,
                root_field_names_stack,
                current_root_field_name
            )

        join = ''.join(texts)
        return join.replace('\'', '"')
