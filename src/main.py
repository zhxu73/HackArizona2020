#!/usr/bin/env python3
import json


with open("aa_example.json") as infile:
    content = infile.read()
    json_obj = json.loads(content)
    json_formatted_str = json.dumps(json_obj, indent=2)
    print(json_formatted_str)

