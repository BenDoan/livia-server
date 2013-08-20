import time
import json

def parsejson(jsonstring):
    data = json.loads(jsonstring)
    if type(data) is dict :
        if "timestamp" in data and "logger" in data and "data" in data :
            if type(data["timestamp"]) is int and type(data["logger"]) is int :
                data["data"]=json.dumps(data["data"])
                return data
    return None
