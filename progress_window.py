import dearpygui.dearpygui as dpg
from database import ProgressTracker

def save_progress_callback(sender, app_data, user_data):
    # Unpack the tuple passed as user_data
    input_field, progress_tracker, progress_group = user_data

    # Get text from input field
    text = dpg.get_value(input_field)

    # Save to database
    if progress_tracker.save_progress(text):
        # Clear input field
        dpg.set_value(input_field, "")

        # Reload progress group
        dpg.delete_item(progress_group, children_only=True)
        for line in progress_tracker.load_progress():
            dpg.add_text(line, parent=progress_group)

def create_progress_window(width, height, pos, theme=None, font=None):
    # Create progress tracker
    progress_tracker = ProgressTracker()

    # Create the progress tracking window
    with dpg.window(
        tag="Progress Window", 
        label="Progress Tracker", 
        width=width, 
        height=height,
        pos=pos,
        no_close=True,
        no_resize=True
    ):
        # Apply global theme if provided
        if theme:
            dpg.bind_theme(theme)

        # Apply font if loaded
        if font:
            dpg.bind_font(font)
        
        

        dpg.add_text("Enter your progress:")
        dpg.add_checkbox(label="Project", tag="R1")
        # Input field
        input_field = dpg.add_input_text(width=-1, hint="Write your progress here...")

        # Progress group
        progress_group = dpg.add_group(tag="progress_group")

        # Initially load existing progress
        for line in progress_tracker.load_progress():
            dpg.add_text(line, parent=progress_group)

        # Save progress button
        dpg.add_button(
            label="Save Progress",
            callback=save_progress_callback,
            user_data=(input_field, progress_tracker, progress_group),
        )