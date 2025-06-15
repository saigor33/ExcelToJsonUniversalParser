from AliasFuncs import Logger
from typing import Optional


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
        missing_arg_names_by_path: Optional[dict[str, str]] = None

        texts: list[str] = []
        for i, item in enumerate(self.items):
            item_type = type(item)
            if item_type == ArgItem:
                arg_item: ArgItem = item
                if arg_item.arg_name in alias_func_args:
                    used_arg_names.add(arg_item.arg_name)
                    texts.append(alias_func_args[arg_item.arg_name])
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
