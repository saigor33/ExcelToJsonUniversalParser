class ParsingConfig:
    def __init__(self,
                 start_parsing_row_index: int,
                 ignore_column_name: str,
                 link_id_column_name: str,
                 field_name_column_name: str,
                 field_value_type_column_name: str,
                 field_value_column_name: str,
                 alias_func_arg_value_column_name: str,
                 ordered_by_level_sheet_names: list[str]
                 ):
        self.start_parsing_row_index = start_parsing_row_index
        self.ignore_column_name = ignore_column_name
        self.link_id_column_name = link_id_column_name
        self.field_name_column_name = field_name_column_name
        self.field_value_type_column_name = field_value_type_column_name
        self.field_value_column_name = field_value_column_name
        self.alias_func_arg_value_column_name = alias_func_arg_value_column_name
        self.ordered_by_level_sheet_names = ordered_by_level_sheet_names
