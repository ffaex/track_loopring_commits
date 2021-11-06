import json

def pretty_response(res):
    pretty_response = json.dumps(res, indent=4)
    return pretty_response
