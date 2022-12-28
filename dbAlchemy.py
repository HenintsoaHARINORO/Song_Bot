from itertools import chain

import sqlalchemy as db


class DbSqlAlchemy:
    def __init__(self, dbname="./Database/info.db"):
        self.dbname = dbname
        self.engine = db.create_engine(f'sqlite:///{dbname}', connect_args={'check_same_thread': False}, echo=False)
        self.conn = self.engine.connect()
        self.metadata_obj = db.MetaData()

    def setup(self):
        users = db.Table(
            'users',
            self.metadata_obj,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('message_id', db.BIGINT),
            db.Column('name', db.String),
            db.Column('song', db.String), extend_existing=True
        )
        self.metadata_obj.create_all(self.engine)
        return users

    def add_item(self, message_id, name, song):
        query = db.insert(DbSqlAlchemy.setup(self)).values(message_id=message_id, name=name, song=song)
        self.conn.execute(query)

    def len_items(self, message_id):
        query = DbSqlAlchemy.setup(self).select().where(DbSqlAlchemy.setup(self).columns.message_id == message_id)
        output = self.conn.execute(query)
        return len(list(output.fetchall()))

    def get_items(self, message_id):
        query = db.select([DbSqlAlchemy.setup(self).c.song]).where(
            DbSqlAlchemy.setup(self).columns.message_id == message_id)
        return iter(chain(*list(self.conn.execute(query).fetchall())))

    def get_last_row(self):
        query = db.select([DbSqlAlchemy.setup(self).c.title, DbSqlAlchemy.setup(self).c.artist]).order_by(
            db.desc(DbSqlAlchemy.setup(self).columns.id))
        return list(self.conn.execute(query).fetchall())
