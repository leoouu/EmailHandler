import sqlite3

DB_PATH = 'resumes.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            file_path TEXT,
            email TEXT,
            content TEXT,
            source TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_resume(name, file_path, email, content, source="manual"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO resumes (name, file_path, email, content, source)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, file_path, email, content, source))
    conn.commit()
    conn.close()

def get_resumes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, file_path, email, content, source FROM resumes')
    resumes = c.fetchall()
    conn.close()
    return resumes

def delete_resume(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM resumes WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def clear_resumes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM resumes')
    conn.commit()
    conn.close()

init_db()
