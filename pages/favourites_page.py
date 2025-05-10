from nicegui import ui
import os
import datafiles.data as data
import ui_nav
from components import create_song_card
from layout import page_with_nav

@page_with_nav("/favourites")
def favourites_page():
    """Favourites page showing user's favourite songs"""
    theme = ui_nav.get_theme_classes()
    
    with ui.column().classes(f"w-full p-0 {theme['bg_main']} min-h-screen"):
        ui.label("Your Favourites").classes(f"text-3xl font-bold {theme['recently_added_text']} my-4 px-4")
        
        # Now playing indicator
        now_playing = ui.label("").classes(f"italic {theme['recently_added_text']} my-2 px-4")
        if data.current_song_id and data.current_song_id in data.songs:
            song_path = data.songs.get(data.current_song_id, "")
            if song_path:
                song_name = os.path.basename(song_path)
                now_playing.set_text(f"Now Playing: {song_name}")
        
        # Function that updates the now playing status
        def update_playing_status(song_name):
            now_playing.set_text(f"Now Playing: {song_name}" if song_name else "")
        
        if not data.favourites:
            ui.label("No favourite songs yet. Add some from the All Songs page!").classes(f"text-xl {theme['text_muted']} italic")
            with ui.link(target="/songs").classes(
                "mt-4 bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded-lg shadow-md transition-all hover:shadow-lg flex items-center gap-2"
            ):
                ui.icon("library_music").classes("text-white")
                ui.label("Browse All Songs").classes("text-white")
        else:
            # Grid container for favorite songs
            with ui.grid(columns=1).classes("w-full gap-0"):
                for song_id, song_path in data.favourites.items():
                    create_song_card(song_id, song_path, True, update_playing_status, with_refresh=True) 