import dearpygui.dearpygui as dpg
from datetime import datetime
from database import ProgressTracker, HabitTracker

def save_progress_callback(sender, app_data, user_data):
    # Rozbalíme progress_tracker, habit_tracker a seznam input fieldů
    progress_tracker, habit_tracker, input_fields, progress_group, streak_text = user_data
    saved_any = False
    
    # Procházíme všechny input fieldy a ukládáme jejich obsah
    for tag, checkbox_tag in input_fields:
        # Kontrolujeme jestli je příslušný checkbox zaškrtnutý
        if dpg.get_value(checkbox_tag) and dpg.is_item_visible(tag):
            text = dpg.get_value(tag)
            if text:  # Pokud pole není prázdné
                # Uložíme text s identifikací checkboxu
                checkbox_label = dpg.get_item_label(checkbox_tag)
                
                # Uložíme do progress trackeru
                progress_tracker.save_progress(f"{checkbox_label}: {text}")
                
                # Označíme, že bylo něco uloženo
                saved_any = True
                
                # Vyčistíme input field
                dpg.set_value(tag, "")
                
    
    # Pokud bylo něco uloženo, aktualizujeme streak
    if saved_any:
        # Uložíme záznam o dnešní aktivitě
        habit_tracker.save_habit(f"Daily progress on {datetime.now().strftime('%Y-%m-%d')}")
        # Obnovíme progress group
        dpg.delete_item(progress_group, children_only=True)
        
        # Načteme a zobrazíme poslední záznamy každého typu
        category_records = {}
        for text, created_at in progress_tracker.load_progress():
            if ":" in text:
                category, content = text.split(":", 1)
                formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.")

                if category not in category_records:
                    category_records[category] = []
                if len(category_records[category]) < 5:
                    category_records[category].append(f"{formatted_date} - {content}")

        # Zobrazíme záznamy podle kategorií
        for category, records in category_records.items():
            if category == "Codewars":
                dpg.add_text(f"Last Kata completed:", parent=progress_group)
            else:
                dpg.add_text(f"Last {category} entries:", parent=progress_group)
            for record in records:
                if category == "Codewars":
                    dpg.add_text(f"  {record} kata", parent=progress_group)
                else:
                    dpg.add_text(f"  {record}", parent=progress_group)
            dpg.add_spacer(height=5, parent=progress_group)
        # Aktualizujeme streak
        streak_count = habit_tracker.get_streak_count()
        dpg.configure_item(streak_text, default_value=f"Current Streak: {streak_count} days")

def checkbox_callback(sender, app_data, user_data):
    input_field_id = user_data
    # Pokud je checkbox zaškrtnutý, zobrazíme text input
    if app_data:
        dpg.configure_item(input_field_id, show=True)
    else:
        dpg.configure_item(input_field_id, show=False)

def create_progress_window(width, height, pos, theme=None, font=None):
    # Create progress tracker
    progress_tracker = ProgressTracker()
    habit_tracker = HabitTracker()
    
    # Seznam input fieldů a jejich příslušných checkboxů pro pozdější použití v save_progress_callback
    input_fields = []
    
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
        
        # Checkbox Project
        with dpg.group(horizontal=True):
            project_checkbox = dpg.add_checkbox(
                label="Project", 
                tag="R1", 
                callback=checkbox_callback, 
                user_data="project_input"
            )
            
            # Input pole napravo od checkboxu (zpočátku skryté)
            project_input = dpg.add_input_text(
                tag="project_input",
                width=300,
                hint="Write your progress here...",
                show=False
            )
            input_fields.append(("project_input", "R1"))
        
        # Checkbox Codewars
        with dpg.group(horizontal=True):
            codewars_checkbox = dpg.add_checkbox(
                label="Codewars", 
                tag="R2", 
                callback=checkbox_callback, 
                user_data="codewars_input"
            )
            
            # Input pole napravo od checkboxu (zpočátku skryté)
            codewars_input = dpg.add_input_text(
                tag="codewars_input",
                width=300,
                hint="Write number of finished kata here...",
                show=False
            )
            input_fields.append(("codewars_input", "R2"))
        
        # Checkbox Course
        with dpg.group(horizontal=True):
            course_checkbox = dpg.add_checkbox(
                label="Course", 
                tag="R3", 
                callback=checkbox_callback, 
                user_data="course_input"
            )
            
            # Input pole napravo od checkboxu (zpočátku skryté)
            course_input = dpg.add_input_text(
                tag="course_input",
                width=300,
                hint="Write your course progress here...",
                show=False
            )
            input_fields.append(("course_input", "R3"))
        
        # Společné Save tlačítko pod všemi checkboxy
        dpg.add_button(
            label="Save All Progress",
            callback=save_progress_callback,
            user_data=(progress_tracker, habit_tracker, input_fields, "progress_group", "streak_text"),
            width=150
        )
        
        # Text pro zobrazení aktuálního streaku
        streak_text = dpg.add_text(
            f"Current Streak: {habit_tracker.get_streak_count()} days",
            tag="streak_text"
        )
        
        # Progress group pod všemi checkboxy a streakem
        progress_group = dpg.add_group(tag="progress_group")
        
        # Načteme a zobrazíme poslední záznamy každého typu
        category_records = {}
        for text, created_at in progress_tracker.load_progress():
            if ":" in text:
                category, content = text.split(":", 1)
                formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.")

                if category not in category_records:
                    category_records[category] = []
                if len(category_records[category]) < 5:
                    category_records[category].append(f"{formatted_date} - {content}")

        # Zobrazíme záznamy podle kategorií
        for category, records in category_records.items():
            if category == "Codewars":
                dpg.add_text(f"Last Kata completed:", parent=progress_group)
            else:
                dpg.add_text(f"Last {category} entries:", parent=progress_group)
            for record in records:
                if category == "Codewars":
                    dpg.add_text(f"  {record} kata", parent=progress_group)
                else:
                    dpg.add_text(f"  {record}", parent=progress_group)
            dpg.add_spacer(height=5, parent=progress_group)
        