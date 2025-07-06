import argparse
import sys
import time
import colorama
import Json.Printer
import ParsingWrapper
import Tests.Benchmark
from JsonAlias import AliasesLoader, Alias
from RowToJsonConverter import AliasFuncResolverFactory
from RowToJsonConverter.Node import Node
from RowToJsonConverter.RefNodesJoiner import RefNodesJoiner
from Sources import SourceWrapperAbstractFactory
from Sources.BaseSourceWrapper import BaseSourceWrapper
from Sources.Configuration.Configs.Config import Config
from Sources.Configuration.ConfigLoader import ConfigLoader
from Tests import ExceptionsHandler


def main(config_file_path: str):
    start_parsing_time = time.time()

    colorama.init()

    config: Config = ConfigLoader(config_file_path).Load()
    json_aliases: dict[str, Alias] = AliasesLoader.load(config.json_aliases_file_paths)

    source_wrapper: BaseSourceWrapper = SourceWrapperAbstractFactory.create(config)

    ref_nodes_joiner = RefNodesJoiner()
    json_printer = Json.Printer.Printer(config.padding_per_layer)

    load_alias_func_nodes_result: ParsingWrapper.LoadResult = \
        ParsingWrapper.load(ref_nodes_joiner, source_wrapper, source_wrapper.getAliasFuncsParsingConfig())

    alias_func_resolver = AliasFuncResolverFactory.create(load_alias_func_nodes_result.nodes_by_feature_name,
                                                          json_aliases)

    load_feature_nodes_result: ParsingWrapper.LoadResult = \
        ParsingWrapper.load(ref_nodes_joiner, source_wrapper, source_wrapper.getFeaturesParsingConfig())

    resolve_alias_funcs_result: ParsingWrapper.ResolveAliasFuncsResult = \
        ParsingWrapper.resolveAliasFuncs(alias_func_resolver, load_feature_nodes_result.nodes_by_feature_name)
    prepared_nodes_by_feature: dict[str, Node] = resolve_alias_funcs_result.nodes_by_feature

    print_jsons_result: ParsingWrapper.PrintJsonsResult = \
        ParsingWrapper.printJsons(config.parsing_features, json_printer, prepared_nodes_by_feature)

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
    parser.add_argument('--print_stacktrace',
                        required=True,
                        type=str,
                        help='Activate print exceptions stacktrace')
    args = parser.parse_args()

    try:
        main(args.config_path)
    except Exception as exception:
        need_print_stacktrace = True if str.lower(args.print_stacktrace) == 'true' else False
        ExceptionsHandler.handle(exception, need_print_stacktrace)
        sys.exit(1)
