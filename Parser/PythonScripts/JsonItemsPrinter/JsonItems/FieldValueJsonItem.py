from JsonItemsPrinter.JsonItems.BaseJsonItem import BaseJsonItem


class FieldValueJsonItem(BaseJsonItem):
    field_name: str
    operator_type: str
    field_value: str

    def __init__(self, field_name: str, operator_type: str, field_value: str):
        self.field_name = field_name
        self.operator_type = operator_type
        self.field_value = field_value
