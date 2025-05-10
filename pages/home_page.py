from nicegui import ui
import os
import json
import actions.playmusic as playmusic
import datafiles.data as data
import ui_nav
import actions.search as search
from layout import page_with_nav

def build_main_content():
    """Builds the main content of the home page"""
    theme = ui_nav.get_theme_classes()
    
    with ui.column().classes(f"w-full min-h-screen p-0 {theme['bg_main']} items-center justify-start text-center space-y-2"):
        # Stats section
        with ui.row().classes(f"w-full max-w-full rounded-none md:rounded-xl justify-around {theme['stats_bg']} p-4 shadow-sm"):
            # Total songs
            with ui.column().classes("items-center"):
                ui.label("Total Songs").classes(f"{theme['text_secondary']}")
                ui.label(f"{len(data.songs)}").classes(f"text-2xl font-bold text-purple-700")
            
            # Favorites
            with ui.column().classes("items-center"):
                ui.label("Favorites").classes(f"{theme['text_secondary']}")
                ui.label(f"{len(data.favourites)}").classes("text-2xl font-bold text-pink-600")
            
            # File types
            with ui.column().classes("items-center"):
                extensions = set()
                for path in data.songs.values():
                    ext = os.path.splitext(path)[1].lower()
                    if ext:
                        extensions.add(ext)
                
                ui.label("File Types").classes(f"{theme['text_secondary']}")
                ui.label(f"{len(extensions)}").classes("text-2xl font-bold text-cyan-600")
        
        # Search Whole Computer button 
        with ui.card().classes(f"w-full max-w-full rounded-none md:rounded-xl {theme['stats_bg']} p-4 shadow-md"):
            with ui.row().classes("justify-between items-center"):
                with ui.column().classes("items-start text-left"):
                    ui.label("Find New Music").classes(f"text-xl font-bold {theme['recently_added_text']}")
                    ui.label("Search your computer for music files").classes(f"{theme['text_secondary']} text-sm")
                
                # Loading container
                loading_container = ui.element("div").classes("flex items-center gap-2")
                
                # Search button
                search_btn = ui.button("Search Whole Computer", icon="search").classes(
                    "bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-2 px-6 rounded-lg shadow-md hover:shadow-lg transition-all"
                )
                
                # Function to handle search 
                async def handle_computer_search():
                    # Adding a spinner removing the previous loading container
                    loading_container.clear()
                    with loading_container:
                        ui.spinner(size="lg").classes("text-blue-500")
                        ui.label("Searching...").classes(f"{theme['text_secondary']}")
                    
                    # Disabling every button during search
                    search_btn.disable()
                    
                    # Runing the search function in a background task
                    try:
                        # Using async function so that it will run without blocking the UI
                        async def run_search_task():
                            try:
                                # Call the search function directly from the search.py file
                                result = search.search_songs("*.mp3", "C:/")
                                
                                # Reloading songs after search gets completes
                                data.songs = data.load_songs()
                                
                                # Upon success, clearing the loading container and showing a checkmark
                                loading_container.clear()
                                with loading_container:
                                    ui.icon("check_circle", size="lg").classes("text-green-500")
                                    ui.label(f"Search complete! Found {len(result)} songs.").classes(f"{theme['text_secondary']}")
                                
                                # Notifying the user about the search completion
                                ui.notify(f"Found {len(result)} new songs!", type="positive")
                            except (OSError, json.JSONDecodeError, PermissionError) as e:
                                # Some error handling that might occur like
                                loading_container.clear()
                                with loading_container:
                                    ui.icon("error", size="lg").classes("text-red-500")
                                    ui.label(f"Error: {str(e)}").classes("text-red-500")
                                
                                # Notify user about the kind of error that might have occured
                                ui.notify(f"Error searching for songs: {str(e)}", type="negative")
                            finally:
                                # Re-enabling the button after search is completed
                                search_btn.enable()
                        
                        # Running the search task in background
                        ui.timer(0.1, run_search_task, once=True)
                        
                    except (OSError, RuntimeError) as e:
                        # Re-enable buttons
                        search_btn.enable()
                        
                        # Clearing loading container and showing error
                        loading_container.clear()
                        with loading_container:
                            ui.icon("error", size="lg").classes("text-red-500")
                            ui.label(f"Error: {str(e)}").classes("text-red-500")
                        
                        # Notifying the user about error
                        ui.notify(f"Error searching for songs: {str(e)}", type="negative")
                
                # Connecing the search button to the handler
                search_btn.on_click(handle_computer_search)
        
        # Recently Added section
        ui.label("Recently Added").classes(f"text-3xl font-bold {theme['recently_added_text']} mt-2 px-4 self-start")
        
        # Displaying 3 most recent songs 
        recent_songs = list(data.songs.items())
        recent_songs.sort(reverse=True)  # Sorting by keys which contain timestamps
        recent_songs = recent_songs[:3]  # Taking 3 most recent
        
        if recent_songs:
            with ui.column().classes("w-full max-w-full space-y-0"):
                for song_id, song_path in recent_songs:
                    song_name = os.path.basename(song_path)
                    
                    with ui.card().classes(f"w-full {theme['card_hover']} transition-colors duration-300 rounded-none md:rounded-xl overflow-hidden {theme['card_border']} shadow-sm hover:shadow-md {theme['recently_card_bg']} mx-0"):
                        with ui.row().classes("justify-between items-center p-2 md:p-4"):
                            ui.label(song_name).classes(f"text-base md:text-lg {theme['song_name_color']} truncate")
                            play_btn = ui.button(icon="play_arrow").classes(
                                f"{theme['play_btn_bg']} hover:bg-blue-600 text-white h-8 w-8 md:h-10 md:w-10 min-w-0 rounded-full"
                            ).tooltip("Play this song")
                            
                            def handle_play(s_id=song_id, s_name=song_name):
                                data.current_song_id = s_id
                                playmusic.play_music(s_id, data.songs)
                                ui.notify(f"Playing: {s_name}", color="green")
                                
                            play_btn.on_click(handle_play)
        else:
            ui.label("No songs added yet").classes(f"text-xl {theme['text_muted']} italic")

@page_with_nav("/")
def home():
    """Home page showing stats and recently added songs"""
    build_main_content() 