"""
Handles disk I/O operations for reading and writing player progression JSON files.
"""
import json
import os

SAVE_DIR = "saves"

def get_save_path(slot_index):
    """
    Constructs the exact filepath string for a specific save slot.
    
    Args:
        slot_index (int): The integer index referencing the desired save slot.
        
    Returns:
        str: The full relative path to the target JSON save file.
    """
    return os.path.join(SAVE_DIR, f"save_slot_{slot_index}.json")

def init_save_dir():
    """
    Ensures that the directory intended to store save files exists on disk.
    Creates the directory framework if it is currently absent.
    """
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def load_slot(slot_index):
    """
    Parses and retrieves game progress data from a specified JSON save file.
    
    Args:
        slot_index (int): The index of the slot to load.
        
    Returns:
        dict or None: The parsed JSON dictionary containing game states, or None if no file exists.
    """
    init_save_dir()
    path = get_save_path(slot_index)
    
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
            
    return None

def save_slot(slot_index, data):
    """
    Serializes a dictionary of game progression data into a formatted JSON save file.
    
    Args:
        slot_index (int): The target slot index to overwrite or create.
        data (dict): The game data payload to securely write to disk.
    """
    init_save_dir()
    path = get_save_path(slot_index)
    
    with open(path, "w") as f:
        json.dump(data, f, indent = 4)

def delete_slot(slot_index):
    """
    Permanently removes the JSON save file associated with the given slot from disk.
    
    Args:
        slot_index (int): The exact slot number to delete.
    """
    path = get_save_path(slot_index)
    
    if os.path.exists(path):
        os.remove(path)