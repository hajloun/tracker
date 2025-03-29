import dearpygui.dearpygui as dpg
from datetime import datetime
from database import ProgressTracker, HabitTracker

def save_progress_callback(sender, app_data, user_data):
    progress_tracker, habit_tracker, input_fields, progress_group, streak_labels = user_data
    saved_any = False

    for tag, checkbox_tag in input_fields:
        if dpg.get_value(checkbox_tag) and dpg.is_item_visible(tag):
            text = dpg.get_value(tag)
            if text:
                checkbox_label = dpg.get_item_label(checkbox_tag)
                progress_tracker.save_progress(f"{checkbox_label}: {text}")
                saved_any = True
                dpg.set_value(tag, "")

    if saved_any:
        habit_tracker.increment_streak(None)  # Increment progress streak
        streak_count = habit_tracker.get_streak_count(None)

        # Update progress display
        dpg.delete_item(progress_group, children_only=True)
        category_records = {}
        for text, created_at in progress_tracker.load_progress():
            if ":" in text:
                category, content = text.split(":", 1)
                formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.")
                if category not in category_records:
                    category_records[category] = []
                if len(category_records[category]) < 5:
                    category_records[category].append(f"{formatted_date} - {content}")

        for category, records in category_records.items():
            dpg.add_text(f"Last {category} entries:", parent=progress_group)
            for record in records:
                dpg.add_text(f"  {record}", parent=progress_group)
            dpg.add_spacer(height=5, parent=progress_group)

        # Update the overall progress streak
        progress_streak = habit_tracker.get_streak_count(None)
        dpg.configure_item("progress_streak", default_value=f"Progress Streak: {progress_streak} days")

def checkbox_callback(sender, app_data, user_data):
    input_field_id = user_data
    if app_data:  # Show input field if checkbox is checked
        dpg.configure_item(input_field_id, show=True)
    else:
        dpg.configure_item(input_field_id, show=False)

def create_progress_window(width, height, pos, theme=None, font=None):
    progress_tracker = ProgressTracker()
    habit_tracker = HabitTracker()
    input_fields = []
    streak_labels = {}

    with dpg.window(
        tag="Progress Window",
        label="Progress Tracker",
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

        dpg.add_text("Enter your progress:")

        # Checkbox for Project
        with dpg.group(horizontal=True):
            project_checkbox = dpg.add_checkbox(
                label="Project",
                tag="project_checkbox",
                callback=checkbox_callback,
                user_data="project_input"
            )
            project_input = dpg.add_input_text(
                tag="project_input",
                width=300,
                hint="Write your progress here...",
                show=False
            )
            input_fields.append(("project_input", "project_checkbox"))

        # Checkbox for Codewars
        with dpg.group(horizontal=True):
            codewars_checkbox = dpg.add_checkbox(
                label="Codewars",
                tag="codewars_checkbox",
                callback=checkbox_callback,
                user_data="codewars_input"
            )
            codewars_input = dpg.add_input_text(
                tag="codewars_input",
                width=300,
                hint="Write number of finished kata here...",
                show=False
            )
            input_fields.append(("codewars_input", "codewars_checkbox"))

        # Checkbox for Course
        with dpg.group(horizontal=True):
            course_checkbox = dpg.add_checkbox(
                label="Course",
                tag="course_checkbox",
                callback=checkbox_callback,
                user_data="course_input"
            )
            course_input = dpg.add_input_text(
                tag="course_input",
                width=300,
                hint="Write your course progress here...",
                show=False
            )
            input_fields.append(("course_input", "course_checkbox"))

        def save_progress_callback(sender, app_data, user_data):
            progress_tracker, habit_tracker, input_fields, progress_group, streak_labels = user_data
            saved_any = False

            for tag, checkbox_tag in input_fields:
                if dpg.get_value(checkbox_tag) and dpg.is_item_visible(tag):
                    text = dpg.get_value(tag)
                    if text:
                        checkbox_label = dpg.get_item_label(checkbox_tag)
                        progress_tracker.save_progress(f"{checkbox_label}: {text}")
                        saved_any = True
                        dpg.set_value(tag, "")
                        dpg.configure_item(tag, show=False)
                        dpg.set_value(checkbox_tag, False)

            if saved_any:
                habit_tracker.increment_streak(None)  # Increment progress streak
                streak_count = habit_tracker.get_streak_count(None)
                dpg.configure_item("progress_streak", default_value=f"Progress Streak: {streak_count} days")

                # Update progress display
                dpg.delete_item(progress_group, children_only=True)
                
                # Define the order we want to display categories
                category_order = ["Project", "Codewars", "Course"]
                category_records = {category: [] for category in category_order}
                
                # Load progress data
                for text, created_at in progress_tracker.load_progress():
                    if ":" in text:
                        category, content = text.split(":", 1)
                        formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.")
                        if category in category_records and len(category_records[category]) < 5:
                            category_records[category].append(f"{formatted_date} - {content}")

                # Display entries in the specified order
                for category in category_order:
                    if category == "Codewars":
                        dpg.add_text(f"Last Kata completed:", parent=progress_group)
                    else:
                        dpg.add_text(f"Last {category} entries:", parent=progress_group)
                    
                    for record in category_records[category]:
                        if category == "Codewars":
                            dpg.add_text(f"  {record} kata", parent=progress_group)
                        else:
                            dpg.add_text(f"  {record}", parent=progress_group)
                    dpg.add_spacer(height=5, parent=progress_group)

        dpg.add_button(
            label="Save Progress",
            callback=save_progress_callback,
            user_data=(progress_tracker, habit_tracker, input_fields, "progress_group", streak_labels)
        )
        
        dpg.add_text(f"Progress Streak: {habit_tracker.get_streak_count(None)} days", tag="progress_streak")
        
        # Group for displaying progress entries
        progress_group = dpg.add_group(tag="progress_group")
        
        # Initially load and display existing entries
        category_order = ["Project", "Codewars", "Course"]
        category_records = {category: [] for category in category_order}
        
        for text, created_at in progress_tracker.load_progress():
            if ":" in text:
                category, content = text.split(":", 1)
                formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.")
                if category in category_records and len(category_records[category]) < 5:
                    category_records[category].append(f"{formatted_date} - {content}")

        # Display initial entries in the specified order
        for category in category_order:
            if category == "Codewars":
                dpg.add_text(f"Last Kata completed:", parent=progress_group)
            else:
                dpg.add_text(f"Last {category} entries:", parent=progress_group)
            
            for record in category_records[category]:
                if category == "Codewars":
                    dpg.add_text(f"  {record} kata", parent=progress_group)
                else:
                    dpg.add_text(f"  {record}", parent=progress_group)
            dpg.add_spacer(height=5, parent=progress_group)

