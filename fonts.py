import dearpygui.dearpygui as dpg
import os

def load_custom_font():
    """Load custom font if available"""
    # Specify the path to your font file
    font_paths = [
        "Delius-Regular.ttf",  # Replace with your font path
        os.path.join(os.path.dirname(__file__), "font.ttf"),
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                with dpg.font_registry():
                    # Load the font
                    default_font = dpg.add_font(font_path, 20)
                    return default_font
            except Exception as e:
                print(f"Error loading font: {e}")

    return None