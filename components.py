from nicegui import ui
import actions.playmusic as playmusic
import os
import ui_nav
import datafiles.data as data

def create_song_card(song_id, song_path, is_favourite, update_playing_fn, with_refresh=False):
    """This is a reuseable component for creating a song card. Whenever needed to create a song card, this function can be used."""
    theme = ui_nav.get_theme_classes() #Getting theme 
    song_name = os.path.basename(song_path) #Getting song name from the path
    
    with ui.card().classes(f"w-full {theme['card_hover']} transition-colors duration-300 shadow-sm hover:shadow-md rounded-none md:rounded-xl overflow-hidden {theme['card_border']} {theme['bg_card']} mx-0"):
        with ui.row().classes("justify-between items-center p-2 md:p-4"):
            with ui.column().classes("flex-grow overflow-hidden"):
                ui.label(song_name).classes(f"text-base md:text-lg font-medium {theme['text_primary']} truncate")
                file_path = song_path.replace("\\", "/")
                ui.label(os.path.dirname(file_path)).classes(f"text-xs {theme['text_muted']} truncate max-w-full")
            
            with ui.row().classes("gap-1 md:gap-2 flex-shrink-0"):
                # Buttons with tooltips
                play_btn = ui.button(icon="play_arrow").classes(
                    f"{theme['play_btn_bg']} hover:bg-blue-600 text-white h-8 w-8 md:h-10 md:w-10 min-w-0 transition-transform hover:scale-110 shadow-sm rounded-full"
                ).tooltip("Play")
                
                pause_btn = ui.button(icon="pause").classes(
                    "bg-gray-600 hover:bg-gray-700 text-white h-8 w-8 md:h-10 md:w-10 min-w-0 transition-transform hover:scale-110 shadow-sm rounded-full"
                ).tooltip("Pause")
                
                stop_btn = ui.button(icon="stop").classes(
                    "bg-gray-800 hover:bg-black text-white h-8 w-8 md:h-10 md:w-10 min-w-0 transition-transform hover:scale-110 shadow-sm rounded-full"
                ).tooltip("Stop")
                
                heart_icon = "favorite" if is_favourite else "favorite_border"
                fav_btn = ui.button(icon=heart_icon).classes(
                    "bg-pink-500 hover:bg-pink-600 text-white h-8 w-8 md:h-10 md:w-10 min-w-0 transition-transform hover:scale-110 shadow-sm rounded-full"
                ).tooltip("Add to Favorites" if not is_favourite else "Remove from Favorites")
                
                # Handlers like play, pause, stop, add to favourites. 
                def handle_play_click(s_id=song_id, s_name=song_name):
                    ui_nav.play_song(s_id, s_name, update_playing_fn)
                
                def handle_pause_click():
                    playmusic.pause_music()
                    ui.notify("Paused", color="orange")
                
                def handle_stop_click():
                    playmusic.stop_music()
                    if update_playing_fn:
                        update_playing_fn("")
                    ui.notify("Stopped", color="red")
                
                def handle_fav_click(s_id=song_id, btn=fav_btn):
                    new_icon = ui_nav.toggle_favourite(s_id)
                    btn.props(f"icon={new_icon}")
                    btn.tooltip("Add to Favorites" if new_icon == "favorite_border" else "Remove from Favorites")
                    
                    # If on the favourites page and removing a favourite, refresh
                    if with_refresh and new_icon == "favorite_border":
                        ui.navigate.to("/favourites")
                
                # Connecting all the handlers to the buttons so that they can work
                play_btn.on_click(handle_play_click)
                pause_btn.on_click(handle_pause_click)
                stop_btn.on_click(handle_stop_click)
                fav_btn.on_click(handle_fav_click) 