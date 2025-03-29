import dearpygui.dearpygui as dpg
import ctypes

# Import window modules
from progress_window import create_progress_window
from habit_window import create_habit_window

# Import other necessary modules
from styles import configure_styles
from fonts import load_custom_font

def get_screen_size():
    """Get the primary monitor's screen resolution"""
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def main():
    # Get screen dimensions
    screen_width, screen_height = get_screen_size()

    # Calculate half width for each window
    half_width = screen_width // 2

    # Initialize DearPyGUI
    dpg.create_context()

    # Configure global theme
    global_theme = configure_styles()

    # Try to load custom font
    default_font = load_custom_font()

    # Create progress window (left half)
    create_progress_window(
        width=half_width, 
        height=screen_height, 
        pos=(0, 0), 
        theme=global_theme, 
        font=default_font
    )

    # Create habit window (right half)
    create_habit_window(
        width=half_width, 
        height=screen_height, 
        pos=(half_width, 0), 
        theme=global_theme, 
        font=default_font
    )

    # Configure viewport
    dpg.create_viewport(
        title="Tracker App", width=screen_width, height=screen_height
    )

    # Setup and show viewport
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Attempt to maximize viewport
    dpg.maximize_viewport()

    # Start the application
    dpg.start_dearpygui()
    
    # Destroy context
    dpg.destroy_context()

if __name__ == "__main__":
    main()