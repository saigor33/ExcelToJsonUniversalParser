import time
import Json.Printer
import NodesToJsonItemConverter
import NodesToJsonItemConverter.Converter
import Sources.Excel.Reader.Reader as ExcelReader
from RowToJsonConverter import NodesLayerBuilder, Converter, AliasFuncNodesJoiner
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.Node import Node
from RowToJsonConverter.NodesLayer import NodesLayer
from RowToJsonConverter.RefNodesJoiner import RefNodesJoiner
from Sources.Excel.Configuration.Config import Config
from Sources.Excel.Reader.Row import Row


class LoadResult:
    def __init__(
            self,
            nodes_by_feature_name: dict[str, Node],
            read_rows_duration: float,
            convert_rows_to_nodes_duration: float,
            joined_ref_nodes_duration: float
    ):
        total_duration: float = read_rows_duration + convert_rows_to_nodes_duration + joined_ref_nodes_duration

        self.nodes_by_feature_name = nodes_by_feature_name
        self.total_duration = total_duration
        self.read_rows_duration = read_rows_duration
        self.convert_rows_to_nodes_duration = convert_rows_to_nodes_duration
        self.joined_ref_nodes_duration = joined_ref_nodes_duration


class ResolveAliasFuncsResult:
    def __init__(self, nodes_by_feature: dict[str, Node], duration: float):
        self.nodes_by_feature = nodes_by_feature
        self.duration = duration


class ReadRowsResult:
    def __init__(self, rows_by_sheet_name: dict[str, list[Row]], duration: float):
        self.rows_by_sheet_name = rows_by_sheet_name
        self.duration = duration


class ConvertRowsToNodesResult:
    def __init__(self, nodes_by_sheet_name: dict[str, list[Node]], duration: float):
        self.nodes_by_sheet_name = nodes_by_sheet_name
        self.duration = duration


class JoinRefNodesResult:
    def __init__(self, nodes_by_feature_name: dict[str, Node], duration: float):
        self.nodes_by_feature_name = nodes_by_feature_name
        self.duration = duration


class PrintJsonsResult:
    def __init__(self, print_result_by_feature_name: dict[str, Json.Printer.Result], total_duration: float):
        self.print_result_by_feature_name = print_result_by_feature_name
        self.duration = total_duration


def load(ref_nodes_joiner: RefNodesJoiner, parsing_config: Config.Parsing, excel_file_path: str) -> LoadResult:
    read_rows_result: ReadRowsResult = readExcelRows(excel_file_path, parsing_config)
    convert_rows_to_nodes_result: ConvertRowsToNodesResult = convertRowsToNodes(read_rows_result.rows_by_sheet_name)
    nodes_layer: NodesLayer = NodesLayerBuilder.build(parsing_config.ordered_by_level_sheet_names,
                                                      convert_rows_to_nodes_result.nodes_by_sheet_name)
    joined_ref_nodes_result: JoinRefNodesResult = joinRefNodes(nodes_layer, ref_nodes_joiner)

    return LoadResult(
        joined_ref_nodes_result.nodes_by_feature_name,
        read_rows_result.duration,
        convert_rows_to_nodes_result.duration,
        joined_ref_nodes_result.duration
    )


def resolveAliasFuncs(
        alias_func_resolver: AliasFuncResolver,
        nodes_by_feature_name: dict[str, Node]
) -> ResolveAliasFuncsResult:
    start_time = time.time()

    prepared_nodes_by_feature: dict[str, Node] = {}
    for feature_name, node in nodes_by_feature_name.items():
        alias_func_stack = []
        prepared_node = AliasFuncNodesJoiner.join(feature_name, node, alias_func_resolver, alias_func_stack)
        prepared_nodes_by_feature[feature_name] = prepared_node

    duration: float = time.time() - start_time
    return ResolveAliasFuncsResult(prepared_nodes_by_feature, duration)


def readExcelRows(excel_file_path, parsing_config) -> ReadRowsResult:
    start_time = time.time()

    rows_by_sheet_name: dict[str, list[Row]] = ExcelReader.read(excel_file_path, parsing_config)

    duration: float = time.time() - start_time
    return ReadRowsResult(rows_by_sheet_name, duration)


def joinRefNodes(nodes_layer: NodesLayer, ref_nodes_joiner: RefNodesJoiner) -> JoinRefNodesResult:
    start_time = time.time()

    joined_nodes_by_feature_name: dict[str, Node] = {}
    for node in nodes_layer.nodes:
        feature_name = node.name
        joined_nodes_by_feature_name[feature_name] = ref_nodes_joiner.join(node, nodes_layer.next_nodes_layer)

    duration: float = time.time() - start_time
    return JoinRefNodesResult(joined_nodes_by_feature_name, duration)


def convertRowsToNodes(rows_by_sheet_name: dict[str, list[Row]]) -> ConvertRowsToNodesResult:
    start_time = time.time()

    nodes_by_sheet_name: dict[str, list[Node]] = {}
    for sheet_name, rows in rows_by_sheet_name.items():
        nodes_by_sheet_name[sheet_name] = Converter.convert(sheet_name, rows)

    duration: float = time.time() - start_time
    return ConvertRowsToNodesResult(nodes_by_sheet_name, duration)


def printJsons(parsing_feature_by_feature_name: dict[str, Config.ParsingFeature], json_printer: Json.Printer.Printer,
               nodes_by_feature: dict[str, Node]) -> PrintJsonsResult:
    start_time = time.time()

    duration_by_feature_name: dict[str, Json.Printer.Result] = {}
    for feature_name, parsing_feature in parsing_feature_by_feature_name.items():
        json_item = NodesToJsonItemConverter.Converter.convert(nodes_by_feature[feature_name])
        print_result: Json.Printer = json_printer.print(parsing_feature, json_item)
        duration_by_feature_name[feature_name] = print_result

    duration: float = time.time() - start_time
    return PrintJsonsResult(duration_by_feature_name, duration)
