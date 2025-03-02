import JsonThreeBuilder.JsonNodesJoiner
import JsonThreeBuilder.NodesThreeToJsonThreeConverter
import JsonThreeBuilder.NodesThreeBuilder
from ExcelDataReader.ParsedExcelRow import ParsedExcelRow
from ExcelDataReader.SheetValueReader import SheetValueReader
from ReferenceFieldValueResolver import ReferenceFieldValueResolver


class Builder:
    def __init__(self,
                 nodes_three_builder: JsonThreeBuilder.NodesThreeBuilder.Builder,
                 reference_field_value_resolver: ReferenceFieldValueResolver,
                 nodes_three_to_json_three_converter: JsonThreeBuilder.NodesThreeToJsonThreeConverter.Converter,
                 json_nodes_joiner: JsonThreeBuilder.JsonNodesJoiner.Joiner):
        self.__json_nodes_joiner = json_nodes_joiner
        self.__referenceFieldValueResolver = reference_field_value_resolver
        self.__nodes_three_builder = nodes_three_builder
        self.__nodes_three_to_json_three_converter = nodes_three_to_json_three_converter

    def build(self, sheet_value_reader: SheetValueReader, feature_name: str, field_rows):
        node = self.__nodes_three_builder.build(feature_name, field_rows)
        node = self.__referenceFieldValueResolver.resolve(sheet_value_reader, node)
        json_item = self.__nodes_three_to_json_three_converter.convert(feature_name, node)

        return self.__json_nodes_joiner.join(json_item)
