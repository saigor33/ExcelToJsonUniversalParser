class Config:
    class ParsingExcel:
        def __init__(self, root_field_full_name_column_index, field_name_column_index, value_column_index,
                     fields_separator):
            self.root_field_full_name_column_index = root_field_full_name_column_index
            self.field_name_column_index = field_name_column_index
            self.value_column_index = value_column_index
            self.fields_separator = fields_separator

    class ParsingFeature:
        def __init__(self, excel_sheet_name, output_directory, output_file_name):
            self.excel_sheet_name = excel_sheet_name
            self.output_directory = output_directory
            self.output_file_name = output_file_name

    def __init__(self,
                 excel_file_path,
                 padding_per_layer,
                 parsing_excel_config: ParsingExcel,
                 parsing_feature_configs_by_feature_name):
        self.excel_file_path = excel_file_path
        self.padding_per_layer = padding_per_layer
        self.parsing_excel_config = parsing_excel_config
        self.parsing_features_by_feature_name = parsing_feature_configs_by_feature_name
