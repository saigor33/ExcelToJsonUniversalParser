from pandas import DataFrame

from DataSources.ParsedDataItem import ParsedDataItem


class Item:
    def __init__(self, excel_sheet_data_frame: DataFrame):
        self.excel_sheet_data_frame = excel_sheet_data_frame
        self.__parsed_data_items: list[ParsedDataItem] = []

    def addParsedDataItem(self, parsed_data_item: ParsedDataItem):
        self.__parsed_data_items.append(parsed_data_item)

    def getParsedDataItem(self) -> list[ParsedDataItem]:
        return self.__parsed_data_items
