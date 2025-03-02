from typing import Optional
from Configuration.DelimiterPresetConfig import DelimiterPresetConfig
from JsonItemsPrinter.JsonItems.BaseJsonItem import BaseJsonItem


class ObjectJsonItem(BaseJsonItem):
    field_name: str
    delimiter_preset: DelimiterPresetConfig
    json_items: list[BaseJsonItem]

    def __init__(self, field_name: str, delimiter_preset: Optional[DelimiterPresetConfig],
                 json_items: list[BaseJsonItem]):
        self.field_name = field_name
        self.delimiter_preset = delimiter_preset
        self.json_items = json_items
