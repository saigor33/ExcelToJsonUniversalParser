from DataSources.Excel.SheetValueReader import SheetValueReader
from JsonThreeBuilder.NodeValues.ReadFromExcelNodeValue import ReadFromExcelNodeValue


class ReadFromExcelNodeValueFactory:
    def __init__(self, sheet_value_reader: SheetValueReader, row_index: int):
        self.__row_index = row_index
        self.__sheet_value_reader = sheet_value_reader

    def create(self, column_index: int) -> ReadFromExcelNodeValue:
        return ReadFromExcelNodeValue(self.__sheet_value_reader, self.__row_index, column_index)
