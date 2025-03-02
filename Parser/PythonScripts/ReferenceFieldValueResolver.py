import Configuration.JsonOperatorType
import Configuration.ValueOperatorType
from ExcelDataReader.SheetValueReader import SheetValueReader
from JsonThreeBuilder.Node import Node
from JsonThreeBuilder.NodeValues.BaseNodeValue import BaseNodeValue
from ReadFromExcelNodeValueFactory import ReadFromExcelNodeValueFactory


class RepeatableRowRange:
    def __init__(self, start_index: int, end_index: int):
        self.start_index = start_index
        self.end_index = end_index


class ReferenceFieldValueResolver:
    def __init__(self, parsing_excel_config):
        self.__parsing_excel_config = parsing_excel_config

    def resolve(self, sheet_value_reader: SheetValueReader, feature_name, node: Node):
        return self._Resolve(sheet_value_reader, node)

    def _Resolve(self, sheet_value_reader: SheetValueReader, node: Node):
        if node.nodes is None:
            return node
        else:
            inner_nodes = []

            for inner_node in node.nodes:
                if inner_node.nodes is None:
                    inner_nodes.append(self._Resolve(sheet_value_reader, inner_node))
                else:
                    repeatable_node: Node = self._FindRepeatableNode(inner_node)
                    if repeatable_node is not None:
                        self._ValidateRepeatableLayer(repeatable_node)
                        repeatable_rows_range = self._GetRepeatableRowsRange(repeatable_node)
                        repeatable_values_inner_node = self._GetRepeatableValuesNode(repeatable_node)
                        repeated_nodes = self._RepeatNodes(sheet_value_reader, repeatable_values_inner_node,
                                                           repeatable_rows_range)
                        inner_nodes.extend(repeated_nodes)
                    else:
                        inner_nodes.append(self._Resolve(sheet_value_reader, inner_node))

            node.nodes = inner_nodes
            return node

    def _RepeatNodes(
            self,
            sheet_value_reader: SheetValueReader,
            repeatable_values_node: Node,
            repeatable_rows_range: RepeatableRowRange
    ):
        new_inner_nodes = []
        for row_index in range(repeatable_rows_range.start_index, repeatable_rows_range.end_index + 1):
            repeated_node_field_name = str(row_index)
            read_from_excel_node_value_factory = ReadFromExcelNodeValueFactory(sheet_value_reader, row_index)

            repeated_node = self._RepeatNode(
                read_from_excel_node_value_factory,
                repeated_node_field_name,
                None,
                repeatable_values_node.nodes)

            new_inner_nodes.append(repeated_node)
        return new_inner_nodes

    def _RepeatNode(self, read_from_excel_node_value_factory: ReadFromExcelNodeValueFactory, field_name: str,
                    node_value: BaseNodeValue, inner_nodes):
        if inner_nodes is None:
            # this ended node. Can't repeatable node or can't need resolve
            return Node(field_name, node_value, None)
        else:
            repeated_inner_nodes = []
            inner_node: Node
            for inner_node in inner_nodes:
                if self.__IsReferenceValueOperator(inner_node.field_name):
                    repeated_inner_node = self.ResolveReferenceNode(read_from_excel_node_value_factory, inner_node)
                    repeated_inner_nodes.append(repeated_inner_node)
                else:
                    repeated_inner_node = (
                        self._RepeatNode(
                            read_from_excel_node_value_factory,
                            inner_node.field_name,
                            inner_node.node_value,
                            inner_node.nodes))
                    repeated_inner_nodes.append(repeated_inner_node)

            return Node(field_name, node_value, repeated_inner_nodes)

    @staticmethod
    def _FindRepeatableNode(inner_node):
        if len(inner_node.nodes) != 1:
            return None
        if inner_node.nodes[0].field_name != Configuration.ValueOperatorType.RepeatableNode:
            return None

        return inner_node.nodes[0]

    @staticmethod
    def ResolveReferenceNode(read_from_excel_node_value_factory: ReadFromExcelNodeValueFactory, node: Node):
        ReferenceFieldValueResolver.__ValidateReferenceLayer(node)

        inner_node = node.nodes[0]
        reference_excel_column_number = inner_node.node_value.get()
        reference_excel_column_index = reference_excel_column_number - 1
        reference_resolved_node_value = read_from_excel_node_value_factory.create(reference_excel_column_index)
        return Node(inner_node.field_name, reference_resolved_node_value, None)

    @staticmethod
    def _GetRepeatableRowsRange(node: Node):
        field_name_error_arg = "".join(["field_name:", str(node.field_name)])
        start_row_number = None
        end_row_number = None

        inner_node: Node
        for inner_node in node.nodes:
            if inner_node.field_name == Configuration.ValueOperatorType.RepeatableStartRowIndex:
                if start_row_number is not None:
                    raise Exception("RepeatableStartRowIndex already set", field_name_error_arg)
                if inner_node.nodes is not None:
                    raise Exception("RepeatableStartRowIndex can't have inner nodes", field_name_error_arg)

                start_row_number = inner_node.node_value.get()
            elif inner_node.field_name == Configuration.ValueOperatorType.RepeatableEndRowIndex:
                if end_row_number is not None:
                    raise Exception("RepeatableEndRowIndex already set", field_name_error_arg)
                if inner_node.nodes is not None:
                    raise Exception("RepeatableEndRowIndex can't have inner nodes", field_name_error_arg)

                end_row_number = inner_node.node_value.get()

        if start_row_number is not None and end_row_number is not None:
            start_row_index = start_row_number - 1
            end_row_index = end_row_number - 1
            return RepeatableRowRange(start_row_index, end_row_index)
        else:
            raise Exception(
                "Invalid repeatable row index",
                field_name_error_arg,
                "".join(["start_row_number:", str(start_row_number)]),
                "".join(["end_row_number:", str(end_row_number)])
            )

    @staticmethod
    def _GetRepeatableValuesNode(node: Node):
        for inner_node in node.nodes:
            if inner_node.field_name == Configuration.ValueOperatorType.RepeatableValues:
                return inner_node
        raise Exception("Repeatable values node not found", node)

    @staticmethod
    def __IsReferenceValueOperator(field_value):
        return field_value == Configuration.ValueOperatorType.Ref

    @staticmethod
    def __ValidateReferenceLayer(node):
        if not ReferenceFieldValueResolver.__IsReferenceValueOperator(node.field_name):
            raise Exception("Attempt validated not reference node", node.field_name)
        if len(node.nodes) != 1:
            raise Exception("Invalid referenced node", node.field_name)

    @staticmethod
    def _ValidateRepeatableLayer(node):
        for inner_node in node.nodes:
            field_name = inner_node.field_name
            if (field_name != Configuration.ValueOperatorType.RepeatableValues
                    and field_name != Configuration.ValueOperatorType.RepeatableStartRowIndex
                    and field_name != Configuration.ValueOperatorType.RepeatableEndRowIndex):
                raise Exception("Invalid repeatable layer", field_name)
