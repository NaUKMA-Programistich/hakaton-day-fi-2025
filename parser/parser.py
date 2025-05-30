import json
import glob

class Task:
    def __init__(self, input_value, output_value):
        self.input = input_value
        self.output = output_value

    def __repr__(self):
        return f"Task(input={self.input!r}, output={self.output!r})"

def parse_json_to_tasks(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Task(t['input'], t['output']) for t in data['tasks']]


