from JsonItemsPrinter.JsonItems.BaseJsonItem import BaseJsonItem


class ObjectJsonItem(BaseJsonItem):
    def __init__(self, field_name, delimiter_preset, json_items):
        self.field_name = field_name
        self.delimiter_preset = delimiter_preset
        self.json_items = json_items
