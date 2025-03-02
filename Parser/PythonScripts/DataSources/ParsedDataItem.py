class ParsedDataItem:
    root_field_full_name: str
    root_layers_names: list[str]
    field_name: str
    field_value: str

    def __init__(self, root_field_full_name: str, root_layers_names: list[str], field_name: str, field_value: str):
        self.root_field_full_name = root_field_full_name
        self.root_layers_names = root_layers_names
        self.field_name = field_name
        self.field_value = field_value
