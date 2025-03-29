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
        # Initialize database connection
        self.db_name = db_name
        self.lock = threading.Lock()
        self.create_table()

    def get_connection(self):
        """Create a new connection for each thread"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create habits table if it doesn't exist"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        date DATE NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
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
            
    def get_streak_count(self):
        """Calculate the current streak based on consecutive days"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT date FROM habits ORDER BY date DESC")
                    dates = [datetime.date.fromisoformat(row[0]) for row in cursor.fetchall()]
                    
                    if not dates:
                        return 0
                    
                    today = datetime.date.today()
                    yesterday = today - datetime.timedelta(days=1)
                    
                    # Pokud nejnovější záznam není z dneška ani ze včerejška, streak začíná od nejnovějšího data
                    if dates[0] < yesterday:
                        return 1
                    
                    # Počítáme streak
                    streak = 1
                    current_date = dates[0]
                    
                    for i in range(1, len(dates)):
                        expected_date = current_date - datetime.timedelta(days=1)
                        if dates[i] == expected_date:
                            streak += 1
                            current_date = dates[i]
                        else:
                            break
                    
                    return streak
        except sqlite3.Error as e:
            print(f"Error calculating streak: {e}")
            return 0