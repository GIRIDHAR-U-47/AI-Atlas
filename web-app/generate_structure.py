import os
import json

def get_tree(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = 'directory'
        d['children'] = [get_tree(os.path.join(path, x)) for x in os.listdir(path) if not x.startswith('.')]
        # Sort children: directories first, then files
        d['children'].sort(key=lambda x: (x['type'] != 'directory', x['name']))
    else:
        d['type'] = 'file'
    return d

docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Docs'))
tree = get_tree(docs_path)

output_path = os.path.join(os.path.dirname(__file__), 'structure.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(tree, f, indent=2)

print(f"Generated structure.json at {output_path}")
