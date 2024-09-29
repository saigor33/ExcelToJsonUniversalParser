import JsonThreeBuilder.JsonNodesJoiner
import JsonThreeBuilder.NodesThreeToJsonThreeConverter
import JsonThreeBuilder.NodesThreeBuilder


class Builder:
    def __init__(self,
                 nodes_three_builder: JsonThreeBuilder.NodesThreeBuilder.Builder,
                 nodes_three_to_json_three_converter: JsonThreeBuilder.NodesThreeToJsonThreeConverter.Converter,
                 json_nodes_joiner: JsonThreeBuilder.JsonNodesJoiner.Joiner):
        self.__json_nodes_joiner = json_nodes_joiner
        self.__nodes_three_builder = nodes_three_builder
        self.__nodes_three_to_json_three_converter = nodes_three_to_json_three_converter

    def build(self, feature_name, field_rows):
        node = self.__nodes_three_builder.build(feature_name, field_rows)
        json_item = self.__nodes_three_to_json_three_converter.convert(feature_name, node)

        return self.__json_nodes_joiner.join(json_item)
