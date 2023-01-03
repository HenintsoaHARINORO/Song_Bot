import csv
import json
import datetime
import random

import constant
import pandas as pd
from youtubesearchpython import *
from telebot import TeleBot, types, ContinueHandling
from telebot.callback_data import CallbackData

import database
import dbAlchemy
from CallBackFilter import CallBackFilter

KPOP = database.get_rows_kpop()
ROCK = database.get_rows_rock()
Country = database.get_rows_country()
POP_MUSIC = database.get_rows_pop()

song_titles = {
    "BTS": database.get_song_titles("BTS"),
    "GOT7": database.get_song_titles("GOT7"),
    "MonstaX": database.get_song_titles("MonstaX"),
    "Twice": database.get_song_titles("Twice"),
    "Blackpink": database.get_song_titles("Blackpink"),
    "TheBeatles": database.get_song_titles("TheBeatles"),
    "PinkF": database.get_song_titles("PinkF"),
    "GreenD": database.get_song_titles("GreenD"),
    "TimMcGraw": database.get_song_titles("TimMcGraw"),
    "Aerosmith": database.get_song_titles("Aerosmith"),
    "LinkinP": database.get_song_titles("LinkinP"),
    "TaylorSwift": database.get_song_titles("TaylorSwift"),
    "BensonBoone": database.get_song_titles("BensonBoone"),
    "EdSheeran": database.get_song_titles("EdSheeran"),
    "Adele": database.get_song_titles("Adele"),
    "Beyonce": database.get_song_titles("Beyonce"),
    "GeorgeStrait": database.get_song_titles("GeorgeStrait"),
    "JohnnyCash": database.get_song_titles("JohnnyCash"),
    "GarthBrooks": database.get_song_titles("GarthBrooks"),
    "CarrieUnderwood": database.get_song_titles("CarrieUnderwood")
}
bts = song_titles["BTS"]
got7 = song_titles["GOT7"]
monstaX = song_titles["MonstaX"]
twice = song_titles["Twice"]
blackpink = song_titles["Blackpink"]
the_beatles = song_titles["TheBeatles"]
pinkF = song_titles["PinkF"]
greenD = song_titles["GreenD"]
timMcGraw = song_titles["TimMcGraw"]
aerosmith = song_titles["Aerosmith"]
linkinP = song_titles["LinkinP"]
taylor_swift = song_titles["TaylorSwift"]
benson_boone = song_titles["BensonBoone"]
ed_sheeran = song_titles["EdSheeran"]
adele = song_titles["Adele"]
beyonce = song_titles["Beyonce"]
george = song_titles["GeorgeStrait"]
johnny_cash = song_titles["JohnnyCash"]
garth_brooks = song_titles["GarthBrooks"]
carrie_underwood = song_titles["CarrieUnderwood"]

kpops_factory = CallbackData('kpops_id', prefix='kpops')
rocks_factory = CallbackData('rocks_id', prefix='rocks')
pops_factory = CallbackData('pops_id', prefix='pops')
country_factory = CallbackData('country_id', prefix='country')
bot = TeleBot(constant.API_TOKEN)
markup = types.ReplyKeyboardMarkup(row_width=2)
btn1 = types.KeyboardButton('/KPOP')
btn2 = types.KeyboardButton('/ROCK')
btn3 = types.KeyboardButton('/POP_MUSIC')
btn4 = types.KeyboardButton('/COUNTRY')
markup.add(btn1, btn2, btn3, btn4)
now = datetime.datetime.now()

hideBoard = types.ReplyKeyboardRemove()


def greetings():
    if now.hour < constant.NOON:
        return "Good morning"
    elif constant.NOON <= now.hour < constant.EVENING:
        return "Good afternoon"
    else:
        return "Good evening"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name
    bot.reply_to(message, f"{greetings()} {user} {constant.HEART_EMOJI},\n"
                          f"Welcome to Songs bot!\n"
                          f"Ask me any songs I will find it for you \n"
                          f"{constant.HINT_EMOJI} Type /choose + your song\n"
                          f"{constant.HINT_EMOJI}  Type /help if you need my guides")


@bot.message_handler(commands=['help'])
def message_handler(message):
    if dbAlchemy.len_items(message.chat.id) != 0:
        users_song = dbAlchemy.get_items(message.chat.id)
        songs = '\n'.join(constant.STAR_EMOJI + str(e) for e in users_song)
        bot.send_message(message.chat.id, f"Here are your favorites :\n"
                                          f"{songs}")
    else:
        bot.send_message(message.chat.id, "You are new here")
    bot.send_message(message.chat.id, "Choose your genre of music?", reply_markup=markup)


@bot.message_handler(commands=['choose'])
def send_welcome(message):
    if not message.text[7:].strip():
        bot.send_message(message.chat.id, "Please type /choose followed by the song")
    else:
        return ContinueHandling()


@bot.message_handler(commands=['choose'])
def start2(message: types.Message):
    song = message.text.split(' ', 1)[1]  # get the title /or singer after the command /choose
    videos_search = VideosSearch(song, limit=10, language='en', region='US')
    data = videos_search.result(mode=ResultMode.json)
    d1 = json.loads(data)
    bot.send_message(message.chat.id, "Here is your song")
    song_id = d1["result"][0]["title"]  # extract the title and singer from json
    dbAlchemy.add_item(message.chat.id, message.from_user.first_name, song_id)
    link = d1["result"][0]["link"]  # extract the link
    bot.send_message(message.chat.id, link)


# suggests to the user by genre of music
@bot.message_handler(commands=['KPOP'])
def suggest_bands(message: types.Message):
    bot.send_message(message.chat.id, 'KPOP BANDS:', reply_markup=kpop_keyboard())


@bot.message_handler(commands=['ROCK'])
def suggest_singers(message: types.Message):
    bot.send_message(message.chat.id, 'ROCK SINGERS:', reply_markup=rock_keyboard())


@bot.message_handler(commands=['POP_MUSIC'])
def start3(message: types.Message):
    bot.send_message(message.chat.id, 'POP Singers:', reply_markup=pop_keyboard())


@bot.message_handler(commands=['COUNTRY'])
def start3(message: types.Message):
    bot.send_message(message.chat.id, 'COUNTRY Singers:', reply_markup=country_keyboard())


@bot.callback_query_handler(func=None, config=kpops_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text
    callback_data1: dict = kpops_factory.parse(callback_data=call.data)

    kpop_id = int(callback_data1['kpops_id']) - 1  # id from database starts at 1
    product = KPOP[kpop_id]

    if product['name'] == "BTS":
        text = f"Here are some titles from {product['name']}:\n {bts}\n"
    elif product['name'] == "Got7":
        text = f"Here are some titles from {product['name']}:\n {got7}\n"
    elif product['name'] == "MONSTA X":
        text = f"Here are some titles from {product['name']}:\n {monstaX}\n"
    elif product['name'] == "Twice":
        text = f"Here are some titles from {product['name']}:\n {twice}\n"
    elif product['name'] == "Blackpink":
        text = f"Here are some titles from {product['name']}:\n {blackpink}\n"

    bot.send_message(chat_id=call.message.chat.id, text=text)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.callback_query_handler(func=None, config=rocks_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text1
    callback_data2: dict = rocks_factory.parse(callback_data=call.data)

    rock_id = int(callback_data2['rocks_id']) - 1

    product1 = ROCK[rock_id]

    if product1['name'] == "The Beatles":
        text1 = f"Here are some titles from {product1['name']}: \n{the_beatles}\n"

    elif product1['name'] == "Pink Floyd":
        text1 = f"Here are some titles from {product1['name']}:\n {pinkF} \n"
    elif product1['name'] == "Green Day":
        text1 = f"Here are some titles from {product1['name']}:\n{greenD} \n"
    elif product1['name'] == "Aerosmith":
        text1 = f"Here are some titles from {product1['name']}:\n {aerosmith} \n"
    elif product1['name'] == "Linkin Park":
        text1 = f"Here are some titles from {product1['name']}:\n{linkinP} \n"
    bot.send_message(chat_id=call.message.chat.id, text=text1)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.callback_query_handler(func=None, config=pops_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text1
    callback_data2: dict = pops_factory.parse(callback_data=call.data)

    pop_id = int(callback_data2['pops_id']) - 1

    product1 = POP_MUSIC[pop_id]

    if product1['name'] == "Taylor Swift":
        text1 = f"Here are some titles from {product1['name']}: \n{taylor_swift}\n"
    elif product1['name'] == "Benson Boone":
        text1 = f"Here are some titles from {product1['name']}:\n {benson_boone} \n"
    elif product1['name'] == "Ed Sheeran":
        text1 = f"Here are some titles from {product1['name']}:\n{ed_sheeran} \n"
    elif product1['name'] == "Adele":
        text1 = f"Here are some titles from {product1['name']}:\n {adele} \n"
    elif product1['name'] == "Beyonce":
        text1 = f"Here are some titles from {product1['name']}:\n{beyonce} \n"
    bot.send_message(chat_id=call.message.chat.id, text=text1)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.callback_query_handler(func=None, config=country_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text1
    callback_data2: dict = country_factory.parse(callback_data=call.data)

    country_id = int(callback_data2['country_id']) - 1

    product1 = Country[country_id]

    if product1['name'] == "Tim McGraw":
        text1 = f"Here are some titles from {product1['name']}: \n{timMcGraw}\n"

    elif product1['name'] == "George Strait":
        text1 = f"Here are some titles from {product1['name']}:\n {george} \n"
    elif product1['name'] == "Johnny Cash":
        text1 = f"Here are some titles from {product1['name']}:\n{johnny_cash} \n"
    elif product1['name'] == "Garth Brooks":
        text1 = f"Here are some titles from {product1['name']}:\n {garth_brooks} \n"
    elif product1['name'] == "Carrie Underwood":
        text1 = f"Here are some titles from {product1['name']}:\n{carrie_underwood} \n"
    bot.send_message(chat_id=call.message.chat.id, text=text1)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.message_handler(func=None, content_types=['text'])
def command_default(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Dear {user_name}\n"
                                      f"I don't understand \" {message.text} \" {constant.WRONG_FACE}\n"
                                      f"Maybe you need /help {constant.CONFUSED_EMOJI}")
    bot.send_message(message.chat.id, f"Or please use the keyboards {constant.KEYBOARD_EMOJI} ")


def kpop_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=kpop_singer['name'],
                    callback_data=kpops_factory.new(kpops_id=kpop_singer["id"])
                )
            ]
            for kpop_singer in KPOP
        ]
    )


def rock_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=rock_singer['name'],
                    callback_data=rocks_factory.new(rocks_id=rock_singer["id"])
                )
            ]
            for rock_singer in ROCK
        ]
    )


def pop_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=pop_artist['name'],
                    callback_data=pops_factory.new(pops_id=pop_artist["id"])
                )
            ]
            for pop_artist in POP_MUSIC
        ]
    )


def country_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=country_artist['name'],
                    callback_data=country_factory.new(country_id=country_artist["id"])
                )
            ]
            for country_artist in Country
        ]
    )


bot.add_custom_filter(CallBackFilter())

bot.infinity_polling()
