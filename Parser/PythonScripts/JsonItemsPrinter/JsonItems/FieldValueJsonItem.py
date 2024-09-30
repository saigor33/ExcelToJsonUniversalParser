from JsonItemsPrinter.JsonItems.BaseJsonItem import BaseJsonItem


class FieldValueJsonItem(BaseJsonItem):
    def __init__(self, field_name, operator_type, field_value):
        self.field_name = field_name
        self.operator_type = operator_type
        self.field_value = field_value
