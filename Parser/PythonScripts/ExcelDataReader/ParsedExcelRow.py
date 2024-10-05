class ParsedExcelRow:
    def __init__(self, root_field_full_name, root_layers_names, original_excel_row):
        self.root_field_full_name = root_field_full_name
        self.root_layers_names = root_layers_names
        self.original_excel_row = original_excel_row
