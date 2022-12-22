import sqlite3
import pandas as pd


class DB:
    def __init__(self, dbname="./Database/save.txt"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS users (message_id,name,song)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, message_id, name, song):
        stmt = "INSERT INTO users (message_id,name,song) VALUES (?,?,?)"
        arg = (message_id, name, song)
        clients = pd.read_sql('SELECT * FROM users', self.conn)
        clients.to_csv('./Database/csvdata.csv', index=False)
        self.conn.execute(stmt, arg)
        self.conn.commit()

    def get_id(self, message_id):
        stmt = "SELECT message_id FROM users where message_id == message_id"
        return [x[0] for x in self.conn.execute(stmt)]

    def get_items(self, message_id):
        clients = pd.read_sql('SELECT * FROM users', self.conn)
        clients.to_csv('./Database/csvdata.csv', index=False)
        stmt = "SELECT song FROM users where message_id == message_id"
        return [x[0] for x in self.conn.execute(stmt)]
