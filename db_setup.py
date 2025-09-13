import sqlite3

# Create database + table
conn = sqlite3.connect("messages.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user TEXT,
              message BLOB)''')
conn.commit()
conn.close()
