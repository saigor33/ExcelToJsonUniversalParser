from prettytable import PrettyTable

import NodesLoader


def printBenchmarks(
        load_alias_func_nodes_result: NodesLoader.LoadResult,
        load_feature_nodes_result: NodesLoader.LoadResult,
        print_json_result: NodesLoader.PrintJsonsResult,
        total_parsing_duration
):
    print_features_benchmarks = _GeneratePrintFeaturesBenchmarks(print_json_result)
    print_features_duration = print_json_result.duration

    benchmarks = PrettyTable()
    benchmarks.field_names = ["Step name", "Description", "Duration (seconds)"]

    _AddBenchmark(benchmarks, "Alias funcs load", "", load_alias_func_nodes_result.total_duration, True)
    _AddBenchmark(benchmarks, "Read Excel", "", load_feature_nodes_result.read_rows_duration, True)
    _AddBenchmark(benchmarks, "Convert excel rows", "", load_feature_nodes_result.convert_rows_to_nodes_duration, True)
    _AddBenchmark(benchmarks, "Join nodes", "", load_feature_nodes_result.joined_ref_nodes_duration, True)
    _AddBenchmark(benchmarks, "Print features", str(print_features_benchmarks), print_features_duration, True)
    _AddBenchmark(benchmarks, "Total duration", "Total parsing duration", total_parsing_duration, True)

    print("".join([str(benchmarks)]))


def _GeneratePrintFeaturesBenchmarks(print_json_result: NodesLoader.PrintJsonsResult) -> PrettyTable:
    benchmarks = PrettyTable()
    benchmarks.field_names = ["Feature name", "Json output path", "Duration (seconds)"]
    for feature_name, print_result in print_json_result.print_result_by_feature_name.items():
        benchmarks.add_row([feature_name, print_result.output_file_path, f"{print_result.duration:.2f}"])

    return benchmarks


def _AddBenchmark(benchmarks: PrettyTable, step_name: str, description: str, duration: float, divider: bool):
    benchmarks.add_row([step_name, description, f"{duration:.2f}"], divider=divider)
