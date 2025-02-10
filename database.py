import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('sport.db')
    c = conn.cursor()
    
    # Пользователи
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user')''')
    
    # Инвентарь
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity INTEGER,
                condition TEXT,
                price REAL)''')
    
    # Тестовый администратор
    if not c.execute("SELECT * FROM users WHERE email='admin@example.com'").fetchone():
        hashed_password = hash_password('admin123')
        c.execute('''INSERT INTO users (username, email, password, role)
                     VALUES (?, ?, ?, ?)''',
                     ('admin', 'admin@example.com', hashed_password, 'admin'))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password, role):
    try:
        conn = sqlite3.connect('sport.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''SELECT * FROM users 
                     WHERE email = ? AND password = ? AND role = ?''',
                     (email, hash_password(password), role))
        return c.fetchone()
    finally:
        conn.close()

def create_user(username, email, password):
    try:
        conn = sqlite3.connect('sport.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, email, password)
                     VALUES (?, ?, ?)''',
                     (username, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_inventory():
    conn = sqlite3.connect('sport.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    return c.fetchall()