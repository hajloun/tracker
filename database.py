import dearpygui.dearpygui as dpg
import sqlite3
import threading

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
        """Load all progress entries"""
        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT text FROM progress ORDER BY created_at DESC")
                    return [row[0] for row in cursor.fetchall()]
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
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database creation error: {e}")

    def save_habit(self, text):
        """Save habit text to database"""
        if not text.strip():
            return False

        try:
            with self.lock:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO habits (text) VALUES (?)", (text,))
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
                    cursor.execute("SELECT text FROM habits ORDER BY created_at DESC")
                    return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error loading habits: {e}")
            return []