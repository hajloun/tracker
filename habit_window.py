import sqlite3
import dearpygui.dearpygui as dpg
from datetime import datetime
from database import HabitTracker

def save_habit_callback(sender, app_data, user_data):
    """Increment streaks for all habits and refresh the habit group."""
    habit_tracker, habit_group, habit_labels = user_data

    # Increment streaks for all habits
    habits = ["Meditation", "Reading", "No Social Media", "No Porn"]
    for habit in habits:
        habit_tracker.increment_streak(habit)

    # Refresh the habit group to display updated streaks
    dpg.delete_item(habit_group, children_only=True)
    for line in habit_tracker.load_habits():
        dpg.add_text(line, parent=habit_group)

    # Update streak displays for each habit
    for habit, label_tag in habit_labels.items():
        streak_count = habit_tracker.get_streak_count(habit)
        dpg.configure_item(label_tag, default_value=f"{habit} Streak: {streak_count} days")

def checkbox_callback(sender, app_data, user_data):
    habit_tracker, habit_name = user_data
    if app_data:  # If checkbox is checked
        habit_tracker.increment_streak(habit_name)  # Increment streak for the habit

def create_habit_window(width, height, pos, theme=None, font=None):
    habit_tracker = HabitTracker()

    with dpg.window(
        tag="Habit Window",
        label="Habit Tracker",
        width=width,
        height=height,
        pos=pos,
        no_close=True,
        no_resize=True
    ):
        if theme:
            dpg.bind_theme(theme)
        if font:
            dpg.bind_font(font)

        dpg.add_text("Select your habits:")
        
        # Store habit labels and checkboxes for updating streak display
        habit_labels = {}
        habit_checkboxes = {}
        
        habits = ["Meditation", "Reading", "No Social Media", "No Porn"]
        
        # Create checkboxes and streak displays for each habit
        for habit in habits:
            with dpg.group(horizontal=True):
                habit_checkboxes[habit] = dpg.add_checkbox(label=habit)
                habit_labels[habit] = dpg.add_text(f"{habit} Streak: {habit_tracker.get_streak_count(habit)} days")

        def save_habits_callback():
            for habit in habits:
                # Only increment streak if habit is checked
                if dpg.get_value(habit_checkboxes[habit]):
                    habit_tracker.increment_streak(habit)
                    streak_count = habit_tracker.get_streak_count(habit)
                    dpg.configure_item(habit_labels[habit], default_value=f"{habit} Streak: {streak_count} days")
                    # Uncheck the checkbox after saving
                    dpg.set_value(habit_checkboxes[habit], False)

        dpg.add_button(label="Save Habits", callback=save_habits_callback)

def increment_habit_streak(habit_tracker, habit, habit_labels):
    """Increment the streak for a specific habit and update its label."""
    habit_tracker.increment_streak(habit)
    streak_count = habit_tracker.get_streak_count(habit)
    dpg.configure_item(habit_labels[habit], default_value=f"{habit} Streak: {streak_count} days")