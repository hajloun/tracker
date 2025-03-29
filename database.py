import dearpygui.dearpygui as dpg
import sqlite3
import threading
import datetime

class ProgressTracker:
    def __init__(self, db_name="progress.db"):
        # Initialize database connection
        self.db_name = db_name
        self.lock = threading.Lock()
        self.create_table()

    def get_connection(self):
        """Create a new connection for each thread"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create progress table if it doesn't exist"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Update table creation to ensure all columns exist
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database creation error: {e}")

    def save_progress(self, text):
        """Save progress text to database"""
        if not text.strip():
            return False

        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO progress (text) VALUES (?)", (text,))
                    conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error saving progress: {e}")
            return False

    def load_progress(self):
        """Load all progress entries with timestamps"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT text, created_at FROM progress ORDER BY created_at DESC")
                    return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error loading progress: {e}")
            return []
        
class HabitTracker:
    def __init__(self, db_name="progress.db"):
        self.db_name = db_name
        self.lock = threading.Lock()
        self.create_table()

    def get_connection(self):
        """Create a new connection for each thread"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Table for individual habits
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT NOT NULL,
                        streak_count INTEGER DEFAULT 0,
                        last_updated DATE
                    )
                """)
                # Table for progress streak
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS progress_streak (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        streak_count INTEGER DEFAULT 0,
                        last_updated DATE
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database creation error: {e}")

    def save_habit(self, text):
        """Save habit text to database with today's date"""
        if not text.strip():
            return False

        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    today = datetime.date.today().isoformat()
                    
                    # Nejprve zkontrolujeme, zda už dnes máme záznam
                    cursor.execute("SELECT id FROM habits WHERE date = ?", (today,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Pokud už existuje, pouze aktualizujeme text a created_at
                        cursor.execute(
                            "UPDATE habits SET text = ?, created_at = CURRENT_TIMESTAMP WHERE date = ?", 
                            (text, today)
                        )
                    else:
                        # Jinak vložíme nový záznam
                        cursor.execute(
                            "INSERT INTO habits (text, date) VALUES (?, ?)", 
                            (text, today)
                        )
                    
                    conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error saving habit: {e}")
            return False

    def load_habits(self):
        """Load all habit entries"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT text, date FROM habits ORDER BY date DESC")
                    return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error loading habits: {e}")
            return []
            
    def get_streak_count(self, habit_name=None):
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    if habit_name:
                        cursor.execute("SELECT streak_count FROM habits WHERE habit_name = ?", (habit_name,))
                    else:
                        cursor.execute("SELECT streak_count FROM progress_streak LIMIT 1")
                    
                    result = cursor.fetchone()
                    return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error getting streak count: {e}")
            return 0

    def increment_streak(self, habit_name=None):
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    today = datetime.date.today().isoformat()
                    
                    if habit_name:
                        # Check if habit exists
                        cursor.execute("SELECT streak_count, last_updated FROM habits WHERE habit_name = ?", (habit_name,))
                        result = cursor.fetchone()
                        
                        if result:
                            streak_count, last_updated = result
                            if last_updated != today:
                                streak_count += 1
                                cursor.execute(
                                    "UPDATE habits SET streak_count = ?, last_updated = ? WHERE habit_name = ?",
                                    (streak_count, today, habit_name)
                                )
                        else:
                            # Create new habit record
                            cursor.execute(
                                "INSERT INTO habits (habit_name, streak_count, last_updated) VALUES (?, ?, ?)",
                                (habit_name, 1, today)
                            )
                    else:
                        # Handle progress streak
                        cursor.execute("SELECT streak_count, last_updated FROM progress_streak LIMIT 1")
                        result = cursor.fetchone()
                        
                        if result:
                            streak_count, last_updated = result
                            if last_updated != today:
                                streak_count += 1
                                cursor.execute(
                                    "UPDATE progress_streak SET streak_count = ?, last_updated = ?",
                                    (streak_count, today)
                                )
                        else:
                            cursor.execute(
                                "INSERT INTO progress_streak (streak_count, last_updated) VALUES (?, ?)",
                                (1, today)
                            )
                    conn.commit()
        except sqlite3.Error as e:
            print(f"Error incrementing streak: {e}")