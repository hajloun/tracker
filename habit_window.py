import dearpygui.dearpygui as dpg
from datetime import datetime
from database import HabitTracker

def save_habit_callback(sender, app_data, user_data):
    # Unpack the tuple passed as user_data
    habit_tracker, habit_group = user_data
    
    # Reload habit group
    dpg.delete_item(habit_group, children_only=True)
    for line in habit_tracker.load_habits():
        dpg.add_text(line, parent=habit_group)

def checkbox_callback(sender, app_data, user_data):
    habit_tracker, habit_name = user_data
    if app_data:  # If checkbox is checked
        habit_tracker.save_habit(habit_name)  # Save the habit to the database
    else:  # If checkbox is unchecked
        # Logic to handle unchecking can be added here if needed
        pass

def create_habit_window(width, height, pos, theme=None, font=None):
    # Create habit tracker
    habit_tracker = HabitTracker()

    # Create the habit tracking window
    with dpg.window(
        tag="Habit Window", 
        label="Habit Tracker", 
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

        dpg.add_text("Select your habits:")

        # Checkbox for Meditation
        meditation_checkbox = dpg.add_checkbox(
            label="Meditation", 
            tag="meditation_checkbox", 
            callback=checkbox_callback, 
            user_data=(habit_tracker, "Meditation")
        )

        # Checkbox for Reading
        reading_checkbox = dpg.add_checkbox(
            label="Reading", 
            tag="reading_checkbox", 
            callback=checkbox_callback, 
            user_data=(habit_tracker, "Reading")
        )

        # Checkbox for No Social Media
        no_social_media_checkbox = dpg.add_checkbox(
            label="No Social Media", 
            tag="no_social_media_checkbox", 
            callback=checkbox_callback, 
            user_data=(habit_tracker, "No Social Media")
        )

        # Checkbox for No Porn
        no_porn_checkbox = dpg.add_checkbox(
            label="No Porn", 
            tag="no_porn_checkbox", 
            callback=checkbox_callback, 
            user_data=(habit_tracker, "No Porn")
        )

        # Streak displays for each habit
        meditation_streak = dpg.add_text(
            f"Meditation Streak: {habit_tracker.get_streak_count()} days",
            tag="meditation_streak"
        )
        
        reading_streak = dpg.add_text(
            f"Reading Streak: {habit_tracker.get_streak_count()} days",
            tag="reading_streak"
        )
        
        no_social_media_streak = dpg.add_text(
            f"No Social Media Streak: {habit_tracker.get_streak_count()} days",
            tag="no_social_media_streak"
        )
        
        no_porn_streak = dpg.add_text(
            f"No Porn Streak: {habit_tracker.get_streak_count()} days",
            tag="no_porn_streak"
        )

        # Habit group to display saved habits
        habit_group = dpg.add_group(tag="habit_group")

        # Initially load existing habits
        for line in habit_tracker.load_habits():
            dpg.add_text(line, parent=habit_group)

        # Save habit button (optional, can be removed)
        dpg.add_button(
            label="Refresh Habits",
            callback=save_habit_callback,
            user_data=(habit_tracker, habit_group),
        )