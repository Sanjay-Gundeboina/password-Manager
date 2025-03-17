import sqlite3

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database setup complete.")
