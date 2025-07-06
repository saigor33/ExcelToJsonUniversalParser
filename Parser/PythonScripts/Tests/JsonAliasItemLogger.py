from prettytable import PrettyTable

from JsonAlias.Alias import Item, TextItem, ArgItem


def log(name, items: list[Item]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ['Type', 'Value']
    for item in items:
        item_type = type(item)
        if item_type is TextItem:
            text_item: TextItem = item
            pretty_table.add_row(["TextItem", text_item.text], divider=True)
        elif item_type is ArgItem:
            arg_item: ArgItem = item
            pretty_table.add_row(["ArgItem", arg_item.arg_name], divider=True)
        else:
            pretty_table.add_row(["Unknown", ""])

    print("".join(
        [
            "Log alias item",
            f"\tjsonAliasFunc={name}:"
            f"\t\n"
            f"{str(pretty_table)}"
        ]
    ))
