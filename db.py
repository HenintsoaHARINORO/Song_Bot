import sqlite3
from itertools import chain

import pandas as pd


class DB:
    def __init__(self, dbname="./Database/save.sqlite"):
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
    def len_items(self,message_id):
        return len(list(self.conn.execute("SELECT song FROM users where message_id = %10d" % message_id)))

    def get_items(self, message_id):
        l = list(self.conn.execute("SELECT song FROM users where message_id = %10d" % message_id))
        return iter(chain(*l))


