import sqlite3
import pandas as pd


class DBot:
    def __init__(self, dbname="./Database/save.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (message_id,name,artist,title)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, message_id, name, artist, title):
        stmt = "INSERT INTO users (message_id,name,artist,title) VALUES (?,?,?,?)"
        arg = (message_id, name, artist, title)
        clients = pd.read_sql('SELECT * FROM users', self.conn)
        clients.to_csv('./Database/csvdata.csv', index=False)
        self.conn.execute(stmt, arg)
        self.conn.commit()

    def add_user(self, message_id, name):
        stmt = "INSERT INTO users (message_id,name) VALUES (?,?)"
        arg = (message_id, name)
        clients = pd.read_sql('SELECT * FROM users', self.conn)
        clients.to_csv('./Database/csvdata.csv', index=False)
        self.conn.execute(stmt, arg)
        self.conn.commit()

    def get_id(self, message_id):
        stmt = "SELECT message_id FROM users where message_id == message_id"
        return [x[0] for x in self.conn.execute(stmt)]

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, message_id):
        clients = pd.read_sql('SELECT * FROM users', self.conn)
        clients.to_csv('./Database/csvdata.csv', index=False)
        stmt = "SELECT genre FROM users where message_id == message_id"
        return [x[0] for x in self.conn.execute(stmt)]
