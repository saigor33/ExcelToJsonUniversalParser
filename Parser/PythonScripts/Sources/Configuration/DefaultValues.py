from Sources.Configuration.Configs.DebugConfig import DebugConfig

PaddingPerLayer: str = "    "
Debug: DebugConfig = DebugConfig(need_print_benchmarks=False)
JsonAliasesFilePaths: list[str] = []
AnonymAliasFuncArgNameByColumnName: dict[str, str] = {}
