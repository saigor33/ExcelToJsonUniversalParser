from Sources.BaseSourceWrapper import BaseSourceWrapper
from Sources.Configuration.Configs.ExcelSourceConfig import ExcelSourceConfig
from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.Excel import Reader as ExcelReader
from Sources.Row import Row


class SourceWrapper(BaseSourceWrapper):
    def __init__(self, source_config: ExcelSourceConfig):
        self.__source_config = source_config

    def getFeaturesParsingConfig(self) -> ParsingConfig:
        return self.__source_config.features_parsing

    def getAliasFuncsParsingConfig(self):
        return self.__source_config.alias_funcs_parsing

    def read(self, parsing_config: ParsingConfig) -> dict[str, list[Row]]:
        return ExcelReader.read(self.__source_config.excel_file_path, parsing_config)
