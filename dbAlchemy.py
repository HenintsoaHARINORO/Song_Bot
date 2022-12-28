from itertools import chain

import sqlalchemy as db


# Defining the Engine
class DB:
    def __init__(self):
        self.engine = db.create_engine('sqlite:///./Database/info.db', connect_args={'check_same_thread': False},
                                       echo=False)
        self.conn = self.engine.connect()
        self.metadata_obj = db.MetaData()

    def setup(self):
        users = db.Table(
            'users',
            self.metadata_obj,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('message_id', db.BIGINT),
            db.Column('name', db.String),
            db.Column('artist', db.String),
            db.Column('title', db.String), extend_existing=True
        )
        self.metadata_obj.create_all(self.engine)
        return users

    def add_item(self, message_id, name, artist, title):
        query = db.insert(DB.setup(self)).values(message_id=message_id, name=name, artist=artist, title=title)
        self.conn.execute(query)

    def len_items(self, message_id):
        query = DB.setup(self).select().where(DB.setup(self).columns.message_id == message_id)
        output = self.conn.execute(query)
        return len(list(output.fetchall()))

    def get_items(self, message_id):
        query = db.select([DB.setup(self).c.title]).where(DB.setup(self).columns.message_id == message_id)
        l = list(self.conn.execute(query).fetchall())
        return iter(chain(*l))

    def get_last_row(self):
        query = db.select([DB.setup(self).c.title, DB.setup(self).c.artist]).order_by(
            db.desc(DB.setup(self).columns.id))
        return list(self.conn.execute(query).fetchall())
