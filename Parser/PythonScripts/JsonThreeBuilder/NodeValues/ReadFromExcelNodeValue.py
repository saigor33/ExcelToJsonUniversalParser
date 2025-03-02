from DataSources.Excel.SheetValueReader import SheetValueReader
from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue


class ReadFromExcelNodeValue(BaseNodeValue):
    __sheet_value_reader: SheetValueReader
    __row_index: int
    __column_index: int

    def __init__(self, sheet_value_reader: SheetValueReader, row_index: int, column_index: int):
        self.__sheet_value_reader = sheet_value_reader
        self.__row_index = row_index
        self.__column_index = column_index

    def get(self):
        return self.__sheet_value_reader.readValue(self.__row_index, self.__column_index)
