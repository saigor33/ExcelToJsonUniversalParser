from DataSources.ParsedDataItem import ParsedDataItem
from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue


class ParsedExcelRowNodeValue(BaseNodeValue):
    __parsed_data_item: ParsedDataItem

    def __init__(self, parsed_data_item: ParsedDataItem):
        self.__parsed_data_item = parsed_data_item

    def get(self):
        return self.__parsed_data_item.field_value
