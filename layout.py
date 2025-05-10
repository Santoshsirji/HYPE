from nicegui import ui
import ui_nav

def page_with_nav(path):
    """ This is a decorator to wrap a page function with common navigation and layout
    
    Takes Args:
        path: The URL path for the page
        
    Returns:
        Decorator function that adds common layout to a page function
    """
    def decorator(body_fn):
        @ui.page(path)
        def wrapper():
            theme = ui_nav.get_theme_classes()
            with ui.element("div").classes(f"min-h-screen w-full {theme['page_bg']} overflow-y-auto overflow-x-hidden m-0 p-0"):
                ui_nav.build_navbar()
                body_fn()
        return wrapper
    return decorator 