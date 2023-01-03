from sqlalchemy import create_engine, Column, Integer, String, Table, func, inspect
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

metadata = MetaData()
dbname = "./Database/data.db"
engine = create_engine(f'sqlite:///{dbname}')


class User(object):
    id = None
    name = None

    def __init__(self, name, id):
        self.name = name
        self.id = id


class KPOP(User):
    pass


class BTS(User):
    pass


class GOT7(User):
    pass


class MonstaX(User):
    pass


class Twice(User):
    pass


class Blackpink(User):
    pass


class ROCK(User):
    pass


class TheBeatles(User):
    pass


class PinkF(User):
    pass


class GreenD(User):
    pass


class Aerosmith(User):
    pass


class LinkinP(User):
    pass


class TaylorSwift(User):
    pass


class BensonBoone(User):
    pass


class EdSheeran(User):
    pass


class Adele(User):
    pass


class Beyonce(User):
    pass


class TimMcGraw(User):
    pass


class PopMusic(User):
    pass


class GeorgeStrait(User):
    pass


class JohnnyCash(User):
    pass


class GarthBrooks(User):
    pass


class CarrieUnderwood(User):
    pass


class Country(User):
    pass


tables = ['George Strait', 'Johnny Cash', 'Garth Brooks', 'Carrie Underwood', 'kpop_bands', 'pop_singers',
          'country_singers', 'bts_songs', 'blackpink_songs', 'Adele', 'Tim McGraw', 'Beyonce', 'Ed Sheeran',
          'Benson Boone', 'rock_bands', 'Got7', 'MonstaX_songs', 'GreenDay_songs', 'Aerosmith_songs',
          'LinkinPark_songs', 'Twice', 'TheBeatles', 'PinkF', 'TaylorSwift']
classes = [GeorgeStrait, JohnnyCash, GarthBrooks, CarrieUnderwood, KPOP, PopMusic, Country, BTS, Blackpink, Adele,
           TimMcGraw, Beyonce, EdSheeran, BensonBoone, ROCK, GOT7, MonstaX, GreenD, Aerosmith, LinkinP, Twice,
           TheBeatles, PinkF, TaylorSwift]
for table, cls in zip(tables, classes):
    user_table = Table(table, metadata, Column('id', Integer, primary_key=True), Column('name', String))
    mapper(cls, user_table)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
# Create a list of dictionaries representing the rows you want to insert
data = [{'table': KPOP,
         'rows': [{'name': 'BTS'}, {'name': 'Got7'}, {'name': 'MONSTA X'}, {'name': 'Twice'}, {'name': 'Blackpink'}]},
        {'table': BTS,
         'rows': [{'name': 'Left and Right '}, {'name': 'Run'}, {'name': 'Yet To Come'}, {'name': 'Dynamite'}]},
        {'table': ROCK,
         'rows': [{'name': 'The Beatles'}, {'name': 'Pink Floyd'}, {'name': 'Green Day'}, {'name': 'Aerosmith'},
                  {'name': 'Linkin Park'}]},
        {'table': PopMusic,
         'rows': [{'name': 'Taylor Swift'}, {'name': 'Benson Boone'}, {'name': 'Ed Sheeran'}, {'name': 'Adele'},
                  {'name': 'Beyonce'}]},
        {'table': Country,
         'rows': [{'name': 'Tim McGraw'}, {'name': 'George Strait'}, {'name': 'Johnny Cash'}, {'name': 'Garth Brooks'},
                  {'name': 'Carrie Underwood'}]},
        {'table': GOT7,
         'rows': [{'name': 'Save you'}, {'name': 'Never Ever'}, {'name': 'Thank you'}, {'name': 'Home Run'},
                  {'name': 'Everyday'}]},
        {'table': MonstaX,
         'rows': [{'name': 'One day'}, {'name': 'Shine Forever'}, {'name': 'Fighter'}, {'name': 'Love you'},
                  {'name': 'Rush'}]},
        {'table': Twice, 'rows': [{'name': 'What is Love'}, {'name': 'Signal'}, {'name': 'Fancy'}, {'name': 'Likey'},
                                  {'name': 'Dance the Night Away'}]},
        {'table': Blackpink, 'rows': [{'name': 'Boombayah'}, {'name': 'How you like that'}, {'name': 'Forever young'},
                                      {'name': 'Kill this love'}, {'name': 'Ice Cream'}]},
        {'table': TheBeatles, 'rows': [{'name': 'In my Life'}, {'name': 'Yesterday'}, {'name': 'Come together'},
                                       {'name': 'All you need is Love'}, {'name': 'Something'}]},
        {'table': PinkF,
         'rows': [{'name': 'Time'}, {'name': 'Money'}, {'name': 'Hey You'}, {'name': 'Comfortably Numb'},
                  {'name': 'Learning to Fly'}]},
        {'table': GreenD,
         'rows': [{'name': "American Idiot"}, {'name': "21 Guns"}, {'name': "Wake Me Up When September Ends"},
                  {'name': "Know Your Enemy"}, {'name': "Still Breathing"}]},
        {'table': LinkinP,
         'rows': [{'name': "New Divide"}, {'name': "Numb"}, {'name': "Somewhere I Belong"}, {'name': "One Step Closer"},
                  {'name': "Crawling"}]},
        {'table': Aerosmith,
         'rows': [{'name': "I Don't Want to Miss a Thing"}, {'name': "Amazing"}, {'name': "Cryin'"}, {'name': "Crazy"},
                  {'name': "Love in an Elevator"}]},
        {'table': TaylorSwift, 'rows': [{'name': "Love Story"}, {'name': "Blank Space"}, {'name': "Bad Blood"},
                                        {'name': "I Knew You Were Trouble"}, {'name': "Delicate"}]},
        {'table': BensonBoone,
         'rows': [{'name': "In the Stars"}, {'name': "Better Alone"}, {'name': "Before You"}, {'name': "Ghost Town"},
                  {'name': "Nights like these"}]},
        {'table': EdSheeran, 'rows': [{'name': "Shape of You"}, {'name': "Happier"}, {'name': "Thinking Out Loud"},
                                      {'name': "Castle on the Hill"}, {'name': "Sing"}]},
        {'table': Adele, 'rows': [{'name': "Someone Like You"}, {'name': "Send My Love (To Your New Lover)"},
                                  {'name': "Make You Feel My Love"}, {'name': "Hello"},
                                  {'name': "Set Fire to the Rain"}]},
        {'table': Beyonce,
         'rows': [{'name': "Halo"}, {'name': "Sweet Dreams"}, {'name': "Love On Top"}, {'name': "Drunk In Love"},
                  {'name': "Love Drought"}]},
        {'table': TimMcGraw,
         'rows': [{'name': "Don't Take The Girl"}, {'name': "Something Like That"}, {'name': "It's Your Love"},
                  {'name': "Humble and Kind"}, {'name': "Where the Green Grass Grows"}]},
        {'table': GeorgeStrait,
         'rows': [{'name': "I Cross My Heart"}, {'name': "Carrying Your Love With Me"}, {'name': "Give It Away"},
                  {'name': "Ocean Front Property"}, {'name': "Love Without End, Amen"}]},
        {'table': JohnnyCash,
         'rows': [{'name': "Give My Love to Rose"}, {'name': "Sunday Morning Coming Down"}, {'name': "Personal Jesus"},
                  {'name': "Ring of Fire"}, {'name': "I Walk the Line"}]},
        {'table': GarthBrooks, 'rows': [{'name': "The River"}, {'name': "Shameless"}, {'name': "The River"},
                                        {'name': "If Tomorrow Never Comes"}, {'name': "Standing Outside the Fire"}]},
        {'table': CarrieUnderwood,
         'rows': [{'name': "Good Girl"}, {'name': "Love Wins"}, {'name': "Before He Cheats"}, {'name': "Church Bells"},
                  {'name': "Something in the Water"}]}]
"""
for item in data:
    session.bulk_insert_mappings(item['table'], item['rows'])
    session.commit()
"""


def get_rows_kpop():
    rows = session.query(KPOP.id, KPOP.name).with_entities(KPOP.id, KPOP.name)
    return [dict(row) for row in rows.all()]


def get_rows_rock():
    rows = session.query(ROCK.id, ROCK.name).with_entities(ROCK.id, ROCK.name)
    return [dict(row) for row in rows.all()]


def get_rows_country():
    rows = session.query(Country.id, Country.name).with_entities(Country.id, Country.name)
    return [dict(row) for row in rows.all()]


def get_rows_pop():
    rows = session.query(PopMusic.id, PopMusic.name).with_entities(PopMusic.id, PopMusic.name)
    return [dict(row) for row in rows.all()]


def get_song_titles(artist_name):
    class_name = artist_name
    cls = eval(class_name)
    rows = session.query(cls.name).all()
    db = [' '.join(item) for item in rows]
    return '\n'.join('\U00002b50 ' + str(e) for e in db)
