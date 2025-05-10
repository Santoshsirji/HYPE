from nicegui import ui
import datafiles.data as data
import ui_nav

# Import pages so that they will be available to display  
import pages.home_page as home_page
import pages.songs_page as songs_page       
import pages.favourites_page as favourites_page

# Initializing and running the application
ui_nav.apply_global_styling()
ui.run()
