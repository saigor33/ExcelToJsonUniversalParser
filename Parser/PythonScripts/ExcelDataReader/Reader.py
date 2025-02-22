import pandas
from pandas import DataFrame

from ExcelDataReader.ParsedExcelRow import ParsedExcelRow
from Configuration.Config import Config


class Item:
    def __init__(self, excel_sheet_data_frame: DataFrame):
        self.excel_sheet_data_frame = excel_sheet_data_frame
        self.__parsed_excel_rows = []

    def addParsedExcelRow(self, parsed_excel_row: ParsedExcelRow):
        self.__parsed_excel_rows.append(parsed_excel_row)

    def getParsedExcelRows(self):
        return self.__parsed_excel_rows


class Reader:
    def __init__(self, parsing_excel_config: Config.ParsingExcel, excel_file_path: str):
        self.__parsing_excel_config = parsing_excel_config
        self.__excel_file_path = excel_file_path

    def read(self, feature_names_by_excel_sheet_name):
        excel_file = pandas.ExcelFile(self.__excel_file_path)
        items_by_feature_name = {}

        for excel_sheet_name, feature_names in feature_names_by_excel_sheet_name.items():
            excel_sheet_data_frame = excel_file.parse(excel_sheet_name, header=None)

            for feature_name in feature_names:
                if feature_name in items_by_feature_name:
                    raise Exception(''.join(["ExcelDataReader: feature name already added (", feature_name, ")"]))
                items_by_feature_name[feature_name] = Item(excel_sheet_data_frame)

            for index, row in excel_sheet_data_frame.iterrows():
                root_field_full_name = str(row.iloc[self.__parsing_excel_config.root_field_full_name_column_index])

                split_field_names = root_field_full_name.split(self.__parsing_excel_config.fields_separator)
                if len(split_field_names) > 0:
                    split_feature_name = split_field_names[0]

                    if split_feature_name in items_by_feature_name:
                        parsed_excel_row = ParsedExcelRow(root_field_full_name, split_field_names, row)
                        items_by_feature_name[split_feature_name].addParsedExcelRow(parsed_excel_row)

        return items_by_feature_name
