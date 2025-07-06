from Configuration import FieldValueType
from Json.BaseJsonItem import ObjectJsonItem, ValueFieldJsonItem

Example: ObjectJsonItem = ObjectJsonItem(None, False, [
    # field values
    ValueFieldJsonItem("$type", FieldValueType.String, "TypeXXX"),
    ValueFieldJsonItem("field1", FieldValueType.Number, "12345"),
    ValueFieldJsonItem("field2", FieldValueType.Bool, "true"),
    ValueFieldJsonItem("field3", FieldValueType.Null, ""),
    # object
    ObjectJsonItem("field5", False, []),
    ObjectJsonItem("field6", False, [
        ValueFieldJsonItem("$type", FieldValueType.String, "TypeYYY")
    ]),
    # array
    ObjectJsonItem("field7", True, []),
    ObjectJsonItem("field8", True, [
        ValueFieldJsonItem(None, FieldValueType.String, "TypeYYY")
    ]),
    ObjectJsonItem("field9", True, [
        ObjectJsonItem(None, False, []),
        ObjectJsonItem(None, False, [
            ValueFieldJsonItem("$type", FieldValueType.String, "TypeYYY")
        ]),
    ]),
    # dict
    ObjectJsonItem("field10", False, [
        ValueFieldJsonItem("$dict", FieldValueType.String, "TypeZZZ"),
        ObjectJsonItem("Item1", False, []),
        ObjectJsonItem("Item2", False, []),
        ObjectJsonItem("Item3", False, []),
    ]),
])
