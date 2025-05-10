import json

# Global state
songs = {}
favourites = {}
current_song_id = None
search_term = ""
dark_mode = False

def load_songs():
    """Load songs from data.json file"""
    try:
        return json.load(open("data.json"))
    except:
        return {}

def load_favourites():
    """Load favourites from favourites.json file or create if not exists"""
    try:
        return json.load(open("favourites.json"))
    except:
        return {}

def save_favourites(favourites_data):
    """Save favourites to favourites.json file"""
    try:
        with open("favourites.json", "w") as f:
            json.dump(favourites_data, f, indent=4)
    except:
        pass

def load_settings():
    """Load settings from settings.json file"""
    try:
        settings = json.load(open("settings.json"))
        return settings.get("dark_mode", False)
    except:
        return False

def save_settings(dark_mode_value):
    """Save user settings to settings.json file"""
    try:
        with open("settings.json", "w") as f:
            json.dump({"dark_mode": dark_mode_value}, f, indent=4)
    except:
        pass

# Initializing the data from respective files
songs = load_songs()
favourites = load_favourites()
dark_mode = load_settings() 