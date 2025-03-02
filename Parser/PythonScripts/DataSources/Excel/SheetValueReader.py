from pandas import DataFrame


class SheetValueReader:
    __sheet_data_frame: DataFrame

    def __init__(self, sheet_data_frame: DataFrame):
        self.__sheet_data_frame = sheet_data_frame

    def readValue(self, row_index: int, column_index: int):
        return self.__sheet_data_frame.iloc[row_index, column_index]
