from Sources.Configuration.Configs.ParsingConfig import ParsingConfig
from Sources.Row import Row
import abc


class BaseSourceWrapper(abc.ABC):
    @abc.abstractmethod
    def getFeaturesParsingConfig(self) -> ParsingConfig:
        pass

    @abc.abstractmethod
    def getAliasFuncsParsingConfig(self) -> ParsingConfig:
        pass

    @abc.abstractmethod
    def read(self, parsing_config: ParsingConfig) -> dict[str, list[Row]]:
        pass
