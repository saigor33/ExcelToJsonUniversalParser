import pandas
from colorama import Fore, Style
from prettytable import PrettyTable

from Sources.Excel.Configuration.Config import Config
from Sources.Excel.Reader.Row import Row


class Reader:
    def __init__(self, config: Config):
        self.__config = config

    def read(self) -> dict[str, list[Row]]:
        excel_file = pandas.ExcelFile(self.__config.excel_file_path)
        rows_by_sheet_name = {}

        for sheet_name in self.__config.parsing.ordered_by_level_sheet_names:
            excel_sheet_data_frame = excel_file.parse(sheet_name, header=None, index_col=None)
            rows_by_sheet_name[sheet_name] = self._ReadRows(sheet_name, excel_sheet_data_frame)

        return rows_by_sheet_name

    def _ReadRows(self, sheet_name: str, excel_sheet_data_frame: pandas.DataFrame) -> list[Row]:
        result = []

        index: int
        for index, excel_row in excel_sheet_data_frame.iterrows():
            if index < self.__config.parsing.start_parsing_row_index:
                continue

            if not self._NeedIgnoreRow(sheet_name, index, excel_row):
                lind_id_cell = excel_row.iloc[self.__config.parsing.link_id_column_index]
                field_name_cell = excel_row.iloc[self.__config.parsing.field_name_column_index]
                field_value_type_cell = excel_row.iloc[self.__config.parsing.field_value_type_column_index]
                field_value_cell = excel_row.iloc[self.__config.parsing.field_value_column_index]

                link_id = self.__ReadCellValue(lind_id_cell)
                field_name = self.__ReadCellValue(field_name_cell)
                field_value_type = self.__ReadCellValue(field_value_type_cell)
                field_value = self.__ReadCellValue(field_value_cell)

                is_empty_row = (
                        link_id is None
                        and field_name is None
                        and field_value_type is None
                        and field_value is None)

                if not is_empty_row:
                    result.append(Row(index, link_id, field_name, field_value_type, field_value))

        return result

    def __ReadCellValue(self, cell):
        return str(cell).strip() if not self._IsEmptyCell(cell) else None

    def _NeedIgnoreRow(self, sheet_name: str, row_index: int, excel_row):
        ignore_cell = excel_row.iloc[self.__config.parsing.ignore_column_index]

        if self._IsEmptyCell(ignore_cell):
            return False

        ignore_value = str(ignore_cell).lower()
        if ignore_value == 'true' or ignore_value == '1':
            return True
        if ignore_value == 'false' or ignore_value == '0':
            return False

        print(Fore.YELLOW + 'Warning:  ignore type should be bool.' + Style.RESET_ALL)

        table = PrettyTable()
        table.field_names = ["Sheet name", "Row index", "ignore", ]
        highlighted_ignore_value = "".join([Fore.YELLOW, ignore_value, Style.RESET_ALL])
        table.add_row([sheet_name, row_index, highlighted_ignore_value])
        error: list[str] = [
            '\n' + str(table),
            '\n'
        ]
        print("".join(error))
        return False

    @staticmethod
    def _IsEmptyCell(ignore_value):
        return pandas.isna(ignore_value) or pandas.isnull(ignore_value)
