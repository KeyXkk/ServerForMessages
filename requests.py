import sqlite3

class database():
    def __init__(self):
        self.database = sqlite3.Connection('userdata.db')
        self.cursor = sqlite3.Cursor(self.database)

    def select_all(self):
        return self.cursor.fetchall()       

    def create_user(self, username, name):
        self.cursor.execute("INSERT INTO userdata (username, name) VALUES (?, ?)", (username, name))
        self.database.commit()

    def get_user(self, id):
        self.cursor.execute(f"SELECT * FROM userdata WHERE id = {id}")
        self.database.commit

    def close(self):
        self.database.close()

        
