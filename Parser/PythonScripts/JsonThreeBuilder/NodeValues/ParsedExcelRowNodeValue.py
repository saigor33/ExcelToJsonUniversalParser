from ExcelDataReader.ParsedExcelRow import ParsedExcelRow
from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue


class ParsedExcelRowNodeValue(BaseNodeValue):
    def __init__(self, field_row: ParsedExcelRow, column_index: int):
        self.__field_row = field_row
        self.__column_index = column_index

    def get(self):
        return self.__field_row.original_excel_row.iloc[self.__column_index]
