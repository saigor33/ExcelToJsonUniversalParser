import pandas
from pandas import Series

from DataSources.Excel.Item import Item
from DataSources.ParsedDataItem import ParsedDataItem
from Configuration.Config import Config


class Reader:
    def __init__(self, parsing_excel_config: Config.ParsingExcel, excel_file_path: str):
        self.__parsing_excel_config = parsing_excel_config
        self.__excel_file_path = excel_file_path

    def read(self, feature_names_by_excel_sheet_name) -> dict[str, Item]:
        excel_file = pandas.ExcelFile(self.__excel_file_path)
        items_by_feature_name: dict[str, Item] = {}

        for excel_sheet_name, feature_names in feature_names_by_excel_sheet_name.items():
            excel_sheet_data_frame = excel_file.parse(excel_sheet_name, header=None)

            for feature_name in feature_names:
                if feature_name in items_by_feature_name:
                    raise Exception(''.join(["Excel: feature name already added (", feature_name, ")"]))
                items_by_feature_name[feature_name] = Item(excel_sheet_data_frame)

            row: Series
            for index, row in excel_sheet_data_frame.iterrows():
                root_field_full_name = str(row.iloc[self.__parsing_excel_config.root_field_full_name_column_index])

                split_field_names = root_field_full_name.split(self.__parsing_excel_config.fields_separator)
                if len(split_field_names) > 0:
                    split_feature_name = split_field_names[0]

                    if split_feature_name in items_by_feature_name:
                        # todo: extract in method
                        field_name = str(row.iloc[self.__parsing_excel_config.field_name_column_index])
                        field_value = str(row.iloc[self.__parsing_excel_config.value_column_index])
                        parsed_data_item = (
                            ParsedDataItem(root_field_full_name, split_field_names, field_name, field_value))
                        items_by_feature_name[split_feature_name].addParsedDataItem(parsed_data_item)

        return items_by_feature_name
