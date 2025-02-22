import os
import sys
import JsonItemsPrinter.Printer
import JsonThreeBuilder.Builder
from Configuration.Config import Config
from ExcelDataReader.SheetValueReader import SheetValueReader


class FeatureParser:
    def __init__(self,
                 json_three_converter: JsonThreeBuilder.Builder.Builder,
                 json_items_printer: JsonItemsPrinter.Printer):
        self.__json_three_converter = json_three_converter
        self.__json_items_printer = json_items_printer

    def parse(
            self,
            sheet_value_reader: SheetValueReader,
            parsing_feature_config: Config.ParsingFeature,
            feature_name: str,
            parsed_excel_rows
    ):
        if not os.path.exists(parsing_feature_config.output_directory):
            os.makedirs(parsing_feature_config.output_directory)

        output_file_path = '/'.join([parsing_feature_config.output_directory, parsing_feature_config.output_file_name])

        orig_stdout = sys.stdout
        output_file = open(output_file_path, 'w')
        sys.stdout = output_file

        json_item = self.__json_three_converter.build(sheet_value_reader, feature_name, parsed_excel_rows)
        self.__json_items_printer.print(json_item)

        sys.stdout = orig_stdout
        output_file.close()

        print(''.join(
            [
                "ParsingFeatureFinished:\n",
                "\tFeatureName: ", feature_name, ",\n",
                "\tJsonPath: ", output_file_path
            ]))
