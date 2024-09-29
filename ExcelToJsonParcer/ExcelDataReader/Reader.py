import pandas
from ExcelDataReader.ParsedExcelRow import ParsedExcelRow
from Configuration.Config import Config


class Reader:
    def __init__(self, parsing_excel_config: Config.ParsingExcel, excel_file_path: str):
        self.__parsing_excel_config = parsing_excel_config
        self.__excel_file_path = excel_file_path

    def read(self, feature_names_by_excel_sheet_name):
        excel_file = pandas.ExcelFile(self.__excel_file_path)
        parsed_excel_rows_by_feature_name = {}

        for excel_sheet_name, feature_names in feature_names_by_excel_sheet_name.items():
            excel_sheet_data_frame = excel_file.parse(excel_sheet_name)

            for feature_name in feature_names:
                if feature_name in parsed_excel_rows_by_feature_name:
                    raise Exception(''.join(["ExcelDataReader: feature name already added (", feature_name, ")"]))
                parsed_excel_rows_by_feature_name[feature_name] = []

            for index, row in excel_sheet_data_frame.iterrows():
                root_field_full_name = str(row.iloc[self.__parsing_excel_config.first_column_index])

                split_field_names = root_field_full_name.split(self.__parsing_excel_config.fields_separator)
                if len(split_field_names) > 0:
                    split_feature_name = split_field_names[0]

                    if split_feature_name in parsed_excel_rows_by_feature_name:
                        parsed_excel_row = ParsedExcelRow(root_field_full_name, split_field_names, row)
                        parsed_excel_rows_by_feature_name[split_feature_name].append(parsed_excel_row)

        return parsed_excel_rows_by_feature_name
