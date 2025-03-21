class Config:
    class Parsing:
        def __init__(self,
                     start_parsing_row_index: int,
                     ignore_column_index: int,
                     link_id_column_index: int,
                     field_name_column_index: int,
                     field_value_type_column_index: int,
                     field_value_column_index: int,
                     ordered_by_level_sheet_names: list[str]
                     ):
            self.start_parsing_row_index = start_parsing_row_index
            self.ignore_column_index = ignore_column_index
            self.link_id_column_index = link_id_column_index
            self.field_name_column_index = field_name_column_index
            self.field_value_type_column_index = field_value_type_column_index
            self.field_value_column_index = field_value_column_index
            self.ordered_by_level_sheet_names = ordered_by_level_sheet_names

    class ParsingFeature:
        def __init__(self, output_directory: str, output_file_name: str):
            self.output_directory = output_directory
            self.output_file_name = output_file_name

    def __init__(self, excel_file_path: str, padding_per_layer: str, parsing: Parsing,
                 parsing_features: dict[str, ParsingFeature]):
        self.parsing = parsing
        self.excel_file_path = excel_file_path
        self.padding_per_layer = padding_per_layer
        self.parsing_features = parsing_features
