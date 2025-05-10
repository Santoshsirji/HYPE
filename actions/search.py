import os
import fnmatch
import json
from datetime import datetime

def search_songs(pattern, search_path):
    """
    This function searches for music files matching the pattern in the specified path
    
    Takes Args:
        pattern: File pattern to match (e.g., "*.mp3")
        search_path: Directory to search in
        
    Returns:
        dict: Dictionary of found songs with unique IDs
    """
    matches = []
    data = {}
    counter = 0
    
    # Searching the files in the directory and dumping the data into the data.json file
    for root, dirnames, filenames in os.walk(search_path):
        for filename in fnmatch.filter(filenames, pattern):
            full_path = os.path.join(root, filename)
            matches.append(full_path)
            
            # Create a unique ID based on timestamp and counter
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = f"{timestamp}_{counter}"
            data[unique_id] = full_path
            counter += 1
    
    # Write data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return data
