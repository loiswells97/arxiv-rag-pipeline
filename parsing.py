import json

def parse_metadata(meta_string):
    meta_string = meta_string.strip()
    if not meta_string:
        return meta_string
    try:
        return json.loads(meta_string)
    except json.JSONDecodeError:
        return meta_string