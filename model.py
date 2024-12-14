import sqlite3

database = sqlite3.connect('userdata.db')
cursor = sqlite3.Cursor(database)

cursor.execute("""  id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP""")