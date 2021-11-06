import json

def pretty_response(res):
    pretty_response = json.dumps(res.json(), indent=4)
    return pretty_response

def write_to_file(file_name):
    with open(file_name, 'w') as f:
        f.write(pretty_response)