import argparse
import time
import colorama
import Json.Printer
import NodesLoader
import Tests.Benchmark
from RowToJsonConverter.AliasFuncResolver import AliasFuncResolver
from RowToJsonConverter.Node import Node
from RowToJsonConverter.RefNodesJoiner import RefNodesJoiner
from Sources.Excel.Configuration.Config import Config
from Sources.Excel.Configuration.ConfigLoader import ConfigLoader


def main(config_file_path: str):
    start_parsing_time = time.time()

    colorama.init()

    config: Config = ConfigLoader(config_file_path).Load()

    ref_nodes_joiner = RefNodesJoiner()
    json_printer = Json.Printer.Printer(config.padding_per_layer)

    load_alias_func_nodes_result: NodesLoader.LoadResult = (
        NodesLoader.load(ref_nodes_joiner, config.alias_funcs_parsing, config.excel_file_path))

    alias_func_resolver = AliasFuncResolver(load_alias_func_nodes_result.nodes_by_feature_name)

    load_feature_nodes_result: NodesLoader.LoadResult = \
        NodesLoader.load(ref_nodes_joiner, config.parsing, config.excel_file_path)

    resolve_alias_funcs_result: NodesLoader.ResolveAliasFuncsResult = \
        NodesLoader.ResolveAliasFuncs(alias_func_resolver, load_feature_nodes_result.nodes_by_feature_name)
    prepared_nodes_by_feature: dict[str, Node] = resolve_alias_funcs_result.nodes_by_feature

    print_jsons_result: NodesLoader.PrintJsonsResult = \
        NodesLoader.printJsons(config.parsing_features, json_printer, prepared_nodes_by_feature)

    total_parsing_duration = time.time() - start_parsing_time

    if config.debug.need_print_benchmarks:
        Tests.Benchmark.printBenchmarks(
            load_alias_func_nodes_result,
            load_feature_nodes_result,
            print_jsons_result,
            total_parsing_duration)

    print("\nDone!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excel to Json universal parser')
    parser.add_argument('--config_path',
                        required=True,
                        type=str,
                        help='Path to config.json')
    args = parser.parse_args()

    main(args.config_path)
