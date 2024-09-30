from Configuration.Config import Config
from JsonThreeBuilder.Node import Node


class Builder:
    def __init__(self, parsing_excel_config: Config.ParsingExcel):
        self.__parsing_excel_config = parsing_excel_config

    def build(self, feature_name, field_rows):
        field_name = feature_name
        grouped_rows_by_root_field_name = self.__GroupRowsByRootFieldName(field_rows)

        root_grouped_rows = grouped_rows_by_root_field_name[field_name]
        grouped_rows_by_root_field_name.pop(field_name)
        inner_nodes = self.__Join(field_name, root_grouped_rows, grouped_rows_by_root_field_name)
        node = Node(field_name, None, inner_nodes)

        return node

    def __Join(self, root_field_name, field_rows, grouped_rows_by_root_field_name):
        nodes = []

        for field_row in field_rows:
            field_name = str(field_row.original_excel_row.iloc[self.__parsing_excel_config.second_column_index])
            full_field_name = self.__parsing_excel_config.fields_separator.join([root_field_name, field_name])

            inner_nodes = None
            if full_field_name in grouped_rows_by_root_field_name:
                inner_field_rows = grouped_rows_by_root_field_name[full_field_name]
                grouped_rows_by_root_field_name.pop(full_field_name)
                inner_nodes = self.__Join(full_field_name, inner_field_rows, grouped_rows_by_root_field_name)

            nodes.append(Node(field_name, field_row, inner_nodes))

        return nodes

    @staticmethod
    def __GroupRowsByRootFieldName(field_rows):
        result = {}

        for field_row in field_rows:

            if not field_row.root_field_full_name in result:
                result[field_row.root_field_full_name] = []

            result[field_row.root_field_full_name].append(field_row)

        return result
