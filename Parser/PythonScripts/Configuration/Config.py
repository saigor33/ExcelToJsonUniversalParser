class Config:
    class ParsingExcel:
        root_field_full_name_column_index: int
        field_name_column_index: int
        value_column_index: int
        fields_separator: str

        def __init__(self, root_field_full_name_column_index: int, field_name_column_index: int,
                     value_column_index: int,
                     fields_separator: str):
            self.root_field_full_name_column_index = root_field_full_name_column_index
            self.field_name_column_index = field_name_column_index
            self.value_column_index = value_column_index
            self.fields_separator = fields_separator

    class ParsingFeature:
        excel_sheet_name: str
        output_directory: str
        output_file_name: str

        def __init__(self, excel_sheet_name: str, output_directory: str, output_file_name: str):
            self.excel_sheet_name = excel_sheet_name
            self.output_directory = output_directory
            self.output_file_name = output_file_name

    excel_file_path: str
    padding_per_layer: str
    parsing_excel_config: ParsingExcel
    parsing_features_by_feature_name: dict[str, ParsingFeature]

    def __init__(self,
                 excel_file_path: str,
                 padding_per_layer: str,
                 parsing_excel_config: ParsingExcel,
                 parsing_feature_configs_by_feature_name: dict[str, ParsingFeature]):
        self.excel_file_path = excel_file_path
        self.padding_per_layer = padding_per_layer
        self.parsing_excel_config = parsing_excel_config
        self.parsing_features_by_feature_name = parsing_feature_configs_by_feature_name
