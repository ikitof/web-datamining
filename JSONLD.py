import requests
class JSONLD:
    def __init__(self) :
        pass

    def __new__(cls, context, URL) :
        req = requestAPI(URL)
        return createJSONLD(context, req)
    
def requestAPI(URL) :
    req = requests.get(URL)
    return req.text

def createJSONLD(context,api_json) :
    context_gare =""
    data_context = open(context,'r') 
    try :
        str += data_context
    except Exception as e :
        pass
    context_gare += data_context.read() 
    return context_gare[:-1] + "," + api_json[1:]