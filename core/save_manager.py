import json
import os

SAVE_DIR = "saves"

def get_save_path(slot_index):
    return os.path.join(SAVE_DIR, f"save_slot_{slot_index}.json")

def init_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def load_slot(slot_index):
    init_save_dir()
    path = get_save_path(slot_index)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_slot(slot_index, data):
    init_save_dir()
    path = get_save_path(slot_index)
    with open(path, "w") as f:
        json.dump(data, f, indent = 4)

def delete_slot(slot_index):
    path = get_save_path(slot_index)
    if os.path.exists(path):
        os.remove(path)