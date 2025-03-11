import pandas

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
            rows_by_sheet_name[sheet_name] = self._ReadRows(excel_sheet_data_frame)

        return rows_by_sheet_name

    def _ReadRows(self, excel_sheet_data_frame: pandas.DataFrame) -> list[Row]:
        result = []

        index: int
        for index, excel_row in excel_sheet_data_frame.iterrows():
            ignore_cell = excel_row.iloc[self.__config.parsing.ignore_column_index]
            need_ignore_row = not self._IsEmptyCell(ignore_cell)
            if not need_ignore_row:
                lind_id_cell = excel_row.iloc[self.__config.parsing.link_id_column_index]
                field_name_cell = excel_row.iloc[self.__config.parsing.field_name_column_index]
                field_value_type_cell = excel_row.iloc[self.__config.parsing.field_value_type_column_index]
                field_value_cell = excel_row.iloc[self.__config.parsing.field_value_column_index]

                link_id = str(lind_id_cell).strip() if not self._IsEmptyCell(lind_id_cell) else None
                field_name = str(field_name_cell).strip() if not self._IsEmptyCell(field_name_cell) else None
                field_value_type = str(field_value_type_cell).strip() if not self._IsEmptyCell(
                    field_value_type_cell) else None
                field_value = str(field_value_cell).strip() if not self._IsEmptyCell(field_value_cell) else None

                is_empty_row = (
                        link_id is None
                        and field_name is None
                        and field_value_type is None
                        and field_value is None)

                if not is_empty_row:
                    result.append(Row(index, link_id, field_name, field_value_type, field_value))

        return result

    @staticmethod
    def _IsEmptyCell(ignore_value):
        return pandas.isna(ignore_value) or pandas.isnull(ignore_value)
