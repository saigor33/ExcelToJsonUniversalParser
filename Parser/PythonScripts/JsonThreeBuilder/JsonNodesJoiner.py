import Configuration.ValueOperatorType
import Configuration.JsonOperatorType
from JsonItemsPrinter.JsonItems.ObjectJsonItem import ObjectJsonItem
from JsonItemsPrinter.JsonItems.FieldValueJsonItem import FieldValueJsonItem


class Joiner:
    def join(self, json_item):
        self.__JoinArraysJsonItems(json_item)
        json_item = self.__JoinFieldValueOperatorJsonItems(json_item)
        json_item.field_name = None  # hide feature name in result

        return json_item

    def __JoinFieldValueOperatorJsonItems(self, json_item):
        json_item_type = type(json_item)
        if json_item_type is ObjectJsonItem:
            # all FieldValueJsonItem wrap object field
            object_json_item = json_item
            inner_json_items_count = len(object_json_item.json_items)
            if len(object_json_item.json_items) == 1:
                inner_json_item = object_json_item.json_items[0]

                inner_json_item_type = type(inner_json_item)
                if inner_json_item_type is FieldValueJsonItem:
                    return inner_json_item
                elif inner_json_item_type is ObjectJsonItem:
                    object_json_item.json_items[0] = self.__JoinFieldValueOperatorJsonItems(inner_json_item)
                    return object_json_item
            else:
                for i in range(inner_json_items_count):
                    inner_json_item = object_json_item.json_items[i]
                    object_json_item.json_items[i] = self.__JoinFieldValueOperatorJsonItems(inner_json_item)
                return object_json_item

        elif json_item_type is FieldValueJsonItem:
            return json_item

        else:
            raise Exception(''.join(["Unknown json item type (", str(json_item_type), ")"]))

    def __JoinArraysJsonItems(self, json_item):
        json_item_type = type(json_item)
        if json_item_type is ObjectJsonItem:
            object_json_item = json_item

            if len(object_json_item.json_items) == 1:
                inner_json_item = object_json_item.json_items[0]

                if inner_json_item.field_name == Configuration.JsonOperatorType.Array:
                    object_json_item.json_items = inner_json_item.json_items

                    for i in range(len(object_json_item.json_items)):

                        array_element_json_item = object_json_item.json_items[i]
                        array_element_json_item.field_name = None

                        object_json_item.json_items[i] = array_element_json_item

                        for j in range(len(array_element_json_item.json_items)):
                            array_element_inner_json_item = array_element_json_item.json_items[j]
                            array_element_inner_json_item_type = type(array_element_inner_json_item)

                            if array_element_inner_json_item_type is FieldValueJsonItem:
                                array_element_inner_json_item.field_name = None
                                # don't replase elements because other method replased
                                # root_array_json_item.json_items[i] = array_element_inner_json_item
                            elif array_element_inner_json_item_type is ObjectJsonItem:
                                #     self.__JoinArrayOperatorJsonItems(array_element_json_item)
                                pass
                            else:
                                raise Exception(
                                    ''.join(["Unknown json item type (", str(array_element_inner_json_item_type), ")"]))

                        self.__JoinArraysJsonItems(array_element_json_item)

                else:
                    self.__JoinArraysJsonItems(inner_json_item)

            else:
                for inner_json_item in object_json_item.json_items:
                    self.__JoinArraysJsonItems(inner_json_item)

        elif json_item_type is FieldValueJsonItem:
            pass
        else:
            raise Exception(''.join(["Unknown json item type (", str(json_item_type), ")"]))

    def __JoinArrayOperatorJsonItems(self, json_item):
        json_item_type = type(json_item)
        if json_item_type is ObjectJsonItem:
            object_json_item = json_item

            if len(object_json_item.json_items) == 1:
                inner_json_item = object_json_item.json_items[0]

                if inner_json_item.field_name == Configuration.JsonOperatorType.Array:
                    root_array_json_item = inner_json_item

                    # replace inner item
                    array_elements_count = len(root_array_json_item.json_items)
                    for i in range(array_elements_count):
                        array_element_json_item = root_array_json_item.json_items[i]

                        for j in range(len(array_element_json_item.json_items)):
                            array_element_inner_json_item = array_element_json_item.json_items[j]
                            array_element_inner_json_item_type = type(array_element_inner_json_item)

                            if array_element_inner_json_item_type is FieldValueJsonItem:
                                array_element_inner_json_item.field_name = None
                                # don't replase elements because other method replased
                                # root_array_json_item.json_items[i] = array_element_inner_json_item
                            elif array_element_inner_json_item_type is ObjectJsonItem:
                                array_element_inner_json_item.field_name = None
                                self.__JoinArrayOperatorJsonItems(array_element_json_item)

                    object_json_item.json_items = root_array_json_item.json_items
                else:
                    self.__JoinArrayOperatorJsonItems(inner_json_item)
            else:
                for inner_json_item in json_item.json_items:
                    self.__JoinArrayOperatorJsonItems(inner_json_item)

        elif json_item_type is FieldValueJsonItem:
            pass

        else:
            raise Exception(''.join(["Unknown json item type (", str(json_item_type), ")"]))
