from abc import ABC, abstractmethod


class BaseNodeValue(ABC):
    pass

    @abstractmethod
    def get(self):
        pass
