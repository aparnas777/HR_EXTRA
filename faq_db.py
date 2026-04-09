import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "faq.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Table for tracking user queries to determine frequency
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT UNIQUE NOT NULL,
            frequency INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Table for storing final, approved FAQs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE NOT NULL,
            answer TEXT NOT NULL,
            source TEXT DEFAULT 'admin',  # 'admin' or 'auto_filtered'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_user_query(query_text):
    """Log a query from a user. If it exists, increment its frequency."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Try inserting new, if fails, update frequency
    try:
        cursor.execute("INSERT INTO user_queries (query_text) VALUES (?)", (query_text.strip(),))
    except sqlite3.IntegrityError:
        cursor.execute('''
            UPDATE user_queries 
            SET frequency = frequency + 1, updated_at = CURRENT_TIMESTAMP 
            WHERE query_text = ?
        ''', (query_text.strip(),))
    
    conn.commit()
    conn.close()

def get_frequent_queries(min_frequency=3):
    """Retrieve queries asked at least `min_frequency` times."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, query_text, frequency FROM user_queries WHERE frequency >= ? ORDER BY frequency DESC", 
        (min_frequency,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "query": r[1], "frequency": r[2]} for r in rows]

def add_faq(question, answer, source='admin'):
    """Add a new FAQ."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO faqs (question, answer, source) VALUES (?, ?, ?)", 
            (question.strip(), answer.strip(), source)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # Already exists
    finally:
        conn.close()
    return success

def get_all_faqs():
    """Get all curated FAQs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer, source FROM faqs ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "question": r[1], "answer": r[2], "source": r[3]} for r in rows]

# Initialize the db tables when the module is imported
init_db()