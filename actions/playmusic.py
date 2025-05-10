import pygame
import json

# Initializing Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Trying to open the data.json file and loading the songs data
try:
    with open("data.json", "r") as f:
        content = f.read().strip()
        if not content: #When data.json file is empty
            songs_data = {}
            print("Warning: data.json is empty. Music playback might not work correctly.")
        else:
            # Try to parse JSON
            songs_data = json.loads(content)
except json.JSONDecodeError:
    songs_data = {}
    print("Warning: data.json contains invalid JSON. Music playback might not work correctly.")
except FileNotFoundError:
    songs_data = {}
    print("Warning: data.json not found. Music playback might not work correctly.")
except Exception as e:
    songs_data = {}
    print(f"Warning: Error loading data.json: {e}. Music playback might not work correctly.")

def play_music(music_id, all_songs_data):
    """
    Plays a song by its ID
    
    Takes Args:
        music_id (str): The ID of the song to play
        all_songs_data (dict): Dictionary of all songs
    """
    try:
        # Load songs data if needed
        if not all_songs_data:
            try:
                with open("data.json", "r") as f:
                    content = f.read().strip()
                    if content:
                        songs_data = json.loads(content)
                    else:
                        songs_data = {}
            except FileNotFoundError:
                songs_data = {}
            except json.JSONDecodeError:
                songs_data = {}
            except:
                songs_data = {}
            all_songs_data = songs_data
        
        # Get song path from all_songs_data
        song_to_play = all_songs_data.get(str(music_id))
        if song_to_play:
            # Stop any music that is being played
            pygame.mixer.music.stop()
            # Load and play the song
            pygame.mixer.music.load(song_to_play)
            pygame.mixer.music.play()
        else:
            print(f"Song with ID {music_id} not found.")
    except Exception as e:
        print(f"Error playing music: {str(e)}")

# Function to pause the currently playing music
def pause_music():
    """Pause the currently playing music"""
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    except Exception as e:
        print(f"Error pausing music: {str(e)}")

# Function to unpause the currently paused music
def unpause_music():
    """Resume playing paused music"""
    try:
        pygame.mixer.music.unpause()
    except Exception as e:
        print(f"Error unpausing music: {str(e)}")

def stop_music():
    """Stop the currently playing music"""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error stopping music: {str(e)}")

def get_playback_state():
    if pygame.mixer.music.get_busy():
        return "playing"
    return "stopped_or_paused"

# def set_volume(volume_level):
#     """
#     Setting the volume the volume level
    
#     Args:
#         volume_level (float): Volume level between 0.0 and 1.0
#     """
#     try:
#         volume = max(0.0, min(1.0, volume_level))
#         pygame.mixer.music.set_volume(volume)
#     except Exception as e:
#         print(f"Error setting volume: {str(e)}")
