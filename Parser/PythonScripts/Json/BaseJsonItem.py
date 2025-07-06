from typing import Optional


class BaseJsonItem:
    pass


class ValueFieldJsonItem(BaseJsonItem):
    def __init__(self, field_name: Optional[str], field_value_type: str, field_value: str):
        self.field_name = field_name
        self.field_value_type = field_value_type
        self.field_value = field_value


class ObjectJsonItem(BaseJsonItem):
    def __init__(self, field_name: Optional[str], is_array: bool, json_items: Optional[list[BaseJsonItem]]):
        self.field_name = field_name
        self.is_array = is_array
        self.json_items = json_items
