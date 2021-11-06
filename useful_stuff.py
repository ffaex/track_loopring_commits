import json

def pretty_response(res):
    pretty_response = json.dumps(res, indent=4)
    return pretty_response

def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)