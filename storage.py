# storage.py

import json
from models import StudentGroup

def save_group(group, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(group.to_dict(), f, ensure_ascii=False, indent=2)

def load_group(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return StudentGroup.from_dict(data)


