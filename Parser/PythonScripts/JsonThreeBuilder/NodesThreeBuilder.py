from typing import Optional
from Configuration.Config import Config
from DataSources.ParsedDataItem import ParsedDataItem
from JsonThreeBuilder.Node import Node
from JsonThreeBuilder.NodeValues.ParsedExcelRowNodeValue import ParsedExcelRowNodeValue


class Builder:
    def __init__(self, parsing_excel_config: Config.ParsingExcel):
        self.__parsing_excel_config = parsing_excel_config

    def build(self, feature_name: str, parsed_data_items: list[ParsedDataItem]) -> Node:
        field_name = feature_name
        grouped_parsed_data_items_by_root_field_name: dict[str, list[ParsedDataItem]]
        grouped_parsed_data_items_by_root_field_name = self.__GroupRowsByRootFieldName(parsed_data_items)

        root_grouped_parsed_data_items = grouped_parsed_data_items_by_root_field_name[field_name]
        grouped_parsed_data_items_by_root_field_name.pop(field_name)
        inner_nodes: list[Node] = self.__Join(field_name, root_grouped_parsed_data_items,
                                              grouped_parsed_data_items_by_root_field_name)
        node = Node(field_name, None, inner_nodes)

        return node

    def __Join(
            self,
            root_field_name: str,
            parsed_data_items: list[ParsedDataItem],
            grouped_rows_by_root_field_name: dict[str, list[ParsedDataItem]]
    ) -> list[Node]:
        nodes: list[Node] = []

        parsed_data_item: ParsedDataItem
        for parsed_data_item in parsed_data_items:
            field_name = parsed_data_item.field_name
            full_field_name = self.__parsing_excel_config.fields_separator.join([root_field_name, field_name])

            inner_nodes: Optional[list[Node]] = None
            if full_field_name in grouped_rows_by_root_field_name:
                inner_parsed_data_items: list[ParsedDataItem] = grouped_rows_by_root_field_name[full_field_name]
                grouped_rows_by_root_field_name.pop(full_field_name)
                inner_nodes = self.__Join(full_field_name, inner_parsed_data_items, grouped_rows_by_root_field_name)

            node_value = ParsedExcelRowNodeValue(parsed_data_item)
            nodes.append(Node(field_name, node_value, inner_nodes))

        return nodes

    @staticmethod
    def __GroupRowsByRootFieldName(parsed_data_items: list[ParsedDataItem]) -> dict[str, list[ParsedDataItem]]:
        result = {}

        for parsed_data_item in parsed_data_items:

            if not parsed_data_item.root_field_full_name in result:
                result[parsed_data_item.root_field_full_name] = []

            result[parsed_data_item.root_field_full_name].append(parsed_data_item)

        return result
