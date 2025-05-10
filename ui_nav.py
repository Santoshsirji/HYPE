from nicegui import ui
import datafiles.data as data
import actions.playmusic as playmusic
import os

# Navigation pages for our HYPE app
NAV_ITEMS = [
    ('HOME', '/', 'home', 'bg-green-400'),
    ('ALL SONGS', '/songs', 'library_music', 'bg-purple-400'),
    ('FAVOURITES', '/favourites', 'favorite', 'bg-pink-400'),
]

def get_theme_classes():
    """Returns appropriate color classes based on dark mode setting"""
    if data.dark_mode:
        return {
            "bg_main": "bg-gray-900",
            "bg_card": "bg-gray-800",
            "bg_input": "bg-gray-700",
            "text_primary": "text-white",
            "text_secondary": "text-gray-300",
            "text_muted": "text-gray-400",
            "navbar_bg": "bg-gradient-to-r from-indigo-900 to-purple-900",
            "navbar_btn": "bg-indigo-700 hover:bg-indigo-600",
            "card_hover": "hover:bg-gray-700",
            "btn_group_bg": "bg-indigo-800",
            "search_input_bg": "bg-gray-700",
            "card_border": "border-gray-700",
            "album_icon": "text-purple-400",
            "album_bg": "bg-gray-800",
            "page_bg": "bg-black",
            "stats_bg": "bg-gray-800",
            "recently_added_text": "text-gray-300",
            "recently_card_bg": "bg-gray-800",
            "song_name_color": "text-gray-200",
            "play_btn_bg": "bg-blue-700"
        }
    else:
        return {
            "bg_main": "bg-pink-50",
            "bg_card": "bg-white",
            "bg_input": "bg-white",
            "text_primary": "text-gray-800",
            "text_secondary": "text-gray-700",
            "text_muted": "text-gray-500",
            "navbar_bg": "bg-gradient-to-r from-blue-600 to-purple-600",
            "navbar_btn": "bg-blue-500 hover:bg-blue-400",
            "card_hover": "hover:bg-gray-50",
            "btn_group_bg": "bg-blue-500",
            "search_input_bg": "bg-white",
            "card_border": "border-none",
            "album_icon": "text-purple-600",
            "album_bg": "bg-white",
            "page_bg": "bg-white",
            "stats_bg": "bg-white",
            "recently_added_text": "text-rose-800",
            "recently_card_bg": "bg-white",
            "song_name_color": "text-gray-800",
            "play_btn_bg": "bg-blue-500"
        }

def toggle_dark_mode():
    """Toggles dark mode and saves setting in the settings.json file"""
    data.dark_mode = not data.dark_mode
    data.save_settings(data.dark_mode)
    current_path = ui.context.client.page.path
    ui.navigate.to(current_path)  # Refresh the current page so that the dark mode is applied

def toggle_favourite(song_id):
    """Adds or remove a song from favourites"""
    if song_id in data.favourites:
        del data.favourites[song_id]
        ui.notify(f"Removed from favourites!", color="red")
    else:
        data.favourites[song_id] = data.songs[song_id]
        ui.notify(f"Added to favourites!", color="green")
    
    # Save to file
    data.save_favourites(data.favourites)
    return "favorite" if song_id in data.favourites else "favorite_border"

def play_song(song_id, song_name, update_playing_fn=None):
    """Play a song and update UI accordingly"""
    data.current_song_id = song_id
    
    playmusic.play_music(song_id, data.songs)
    
    if update_playing_fn:
        update_playing_fn(song_name)
    
    ui.notify(f"Playing: {song_name}", color="green")

def build_navbar():
    """Builds the navigation bar with active route highlighting"""
    theme = get_theme_classes()
    active_path = ui.context.client.page.path
    
    with ui.row().classes(f"w-full h-16 md:h-20 {theme['navbar_bg']} px-2 md:px-4 justify-between items-center shadow-lg sticky top-0 left-0 right-0 z-50 overflow-hidden m-0 p-0"):
        # Logo and title
        with ui.row().classes("items-center gap-3 cursor-pointer") as logo_row:
            ui.icon("music_note", size="2rem").classes("text-white")
            ui.label("HYPE").classes("text-white text-3xl font-extrabold tracking-wide")
        
        # On click to logo the app will redirect to home page 
        logo_row.on('click', lambda: ui.navigate.to("/"))
        
        # Center nav links
        with ui.row().classes("flex-grow justify-center"):
            # Use buttons that look like tabs for navigation
            with ui.button_group().classes(f"{theme['btn_group_bg']} rounded-full p-1.5 shadow-md"):
                for label, path, icon_name, active_bg in NAV_ITEMS:
                    is_active = (path == active_path) or (path == "/favourites" and ("/favourite" in active_path or "/favorite" in active_path))
                    link_class = "px-3 md:px-5 py-2 rounded-full font-medium transition-all flex items-center gap-2 " + \
                                (f"{active_bg} text-white shadow-inner font-bold" if is_active else "text-white hover:bg-sky-700")
                    
                    with ui.link(target=path).classes(link_class):
                        ui.icon(icon_name).classes("text-white")
                        ui.label(label).classes("text-white text-sm md:text-base")
        
        # Right section - search and dark mode
        with ui.row().classes("gap-3 items-center"):
            # Search input with button inside a container
            with ui.row().classes("relative"):
                search_input = ui.input(placeholder="Quick search...").classes(
                    f"w-40 md:w-48 h-10 rounded-full pl-4 pr-12 {theme['search_input_bg']} text-gray-800 border-none shadow-sm focus:ring-2 focus:ring-blue-400 transition-all"
                )
                
                # Position search button absolutely to prevent overflow
                with ui.element("div").classes("absolute right-0 top-0 h-full flex items-center pr-1"):
                    search_btn = ui.button(icon="search").classes(
                        f"{theme['navbar_btn']} text-white rounded-full h-8 w-8 min-w-0 shadow-md hover:shadow-lg transition-all"
                    )
            
            # Dark mode toggle functioniality 
            dark_icon = "dark_mode" if not data.dark_mode else "light_mode"
            dark_btn = ui.button(icon=dark_icon).classes(
                f"{theme['navbar_btn']} text-white rounded-full h-10 w-10 min-w-0 shadow-md hover:shadow-lg transition-all duration-300 hover:rotate-12"
            )
            dark_btn.tooltip("Toggle Dark Mode")
            dark_btn.on_click(toggle_dark_mode)
            
            # Badge in the top right corner that shows the total number of songs in the data.json file. 
            with ui.element("div").classes("relative ml-1 group transition-transform hover:scale-110 cursor-pointer"):
                with ui.element("div").classes(f"h-10 w-10 rounded-full flex items-center justify-center {theme['album_bg']} shadow-md"):
                    ui.icon("album", size="1.5rem").classes(f"{theme['album_icon']} transition-all group-hover:text-purple-800")
                ui.badge(str(len(data.songs))).classes("absolute -top-1 -right-1 bg-red-500 text-white font-bold min-w-5 h-5 flex items-center justify-center rounded-full shadow-lg animate-pulse")
                ui.tooltip("Total Songs in Library")
            
            #Search functionality
            def handle_search():
                data.search_term = search_input.value
                ui.navigate.to("/songs")
                
            # When search button is clicked by an user, the handle_search function is called
            search_btn.on_click(handle_search)
            # Also if Enter key is pressed, search will happen
            search_input.on("keydown.enter", handle_search)

def apply_global_styling():
    """Apply global CSS styling to the NiceGUI app"""
    ui.query("body").classes("m-0 p-0 overflow-x-hidden")
    ui.query(".nicegui-content").classes("max-w-none w-full p-0 m-0")
    # Removing default padding in NiceGUI containers so that the app takes the full heignt and width looks clean.  
    ui.query(".nicegui-container").classes("p-0 m-0")
    ui.query(".nicegui-header").classes("p-0 m-0")
    ui.query(".nicegui-content > div").classes("p-0 m-0") 