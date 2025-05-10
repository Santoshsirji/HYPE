from nicegui import ui
import os
import datafiles.data as data
import ui_nav
from components import create_song_card
from layout import page_with_nav

@page_with_nav("/songs")
def songs_page():
    """This page is for displaying all songs. User can also search songs using input box."""

    theme = ui_nav.get_theme_classes()
    
    with ui.column().classes(f"w-full p-0 {theme['bg_main']} min-h-screen"):
        ui.label("All Songs").classes(f"text-3xl font-bold {theme['recently_added_text']} my-4 px-4")
        
        # Label to show which song is currently playing
        now_playing = ui.label("").classes(f"italic {theme['recently_added_text']} my-2 px-4")
        if data.current_song_id and data.current_song_id in data.songs:
            song_path = data.songs.get(data.current_song_id, "")
            if song_path:
                song_name = os.path.basename(song_path)
                now_playing.set_text(f"Now Playing: {song_name}")
        
        # This function will update the now playing label when user selects a song
        def update_playing_status(song_name):
            now_playing.set_text(f"Now Playing: {song_name}" if song_name else "")
        
        # This row contains input field and search button
        with ui.row().classes("w-full mx-0 my-2 px-4 items-center"):
            initial_value = data.search_term
            search_input = ui.input(placeholder="Search songs...", value=initial_value).classes(
                f"w-full p-2 rounded-l-lg border-2 border-r-0 border-purple-300 focus:border-purple-500 focus:outline-none {theme['bg_input']} {theme['text_primary']}"
            )
            search_btn = ui.button(icon="search").classes("bg-purple-600 hover:bg-purple-700 text-white h-10 w-12 rounded-r-lg border-2 border-l-0 border-purple-300")
        
        # We are clearing the global search term after taking it
        data.search_term = ""
        
        # This container will hold all song cards
        songs_container = ui.element('div').classes("w-full")
        
        # This function will filter and show only matching songs
        def filter_songs():
            # First remove all existing song cards
            songs_container.clear()
            
            search_text = search_input.value.lower() if search_input.value else ""
            filtered_songs = {}
            
            # Loop through all songs and check if they match the search
            for song_id, song_path in data.songs.items():
                song_name = os.path.basename(song_path).lower()
                if search_text in song_name:
                    filtered_songs[song_id] = song_path
            
            # Now display filtered results
            with songs_container:
                if filtered_songs:
                    ui.label(f"Found {len(filtered_songs)} songs").classes(f"text-sm {theme['text_muted']} px-4 py-2")
                    with ui.grid(columns=1).classes("w-full gap-0"):
                        for song_id, song_path in filtered_songs.items():
                            is_favourite = song_id in data.favourites
                            create_song_card(song_id, song_path, is_favourite, update_playing_status)
                else:
                    # If no match found, show message and clear option
                    with ui.column().classes("w-full py-6 items-center text-center"):
                        ui.icon("search_off", size="4em").classes(f"{theme['text_muted']} mb-4")
                        ui.label("No songs match your search").classes(f"text-xl {theme['text_muted']} italic")
                        clear_btn = ui.button("Clear Search", icon="clear").classes(
                            "mt-4 bg-rose-600 hover:bg-rose-700 text-white py-2 px-6 rounded-lg"
                        )
                        # On clear button click, reset input and show all songs
                        def clear_search():
                            search_input.set_value("")
                            filter_songs()
                        clear_btn.on_click(clear_search)
        
        # When search button is clicked or Enter is pressed, run filter function
        search_btn.on_click(filter_songs)
        search_input.on("keydown.enter", filter_songs)
        
        # Initially show all songs if no search input is there
        with songs_container:
            with ui.grid(columns=1).classes("w-full gap-0"):
                for song_id, song_path in data.songs.items():
                    is_favourite = song_id in data.favourites
                    create_song_card(song_id, song_path, is_favourite, update_playing_status)
        
        # If user came from navbar with search term, then filter immediately
        if initial_value:
            filter_songs()
