
import json
import datetime
import bson.objectid as bson


def json_serial(obj):
    """
        Transform native data types into serializable types (bson OID, ISO Dates)
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, bson.ObjectId):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


def dic_to_json(doc):
    """
    Convert a dictionary to JSON format
    """
    return json.dumps(doc, default=json_serial)


def body_to_dic(body):
    """
    Convert a JSON to python dict format
    """
    return json.loads(body)
