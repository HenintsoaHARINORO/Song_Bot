import csv
import json
import datetime

from youtubesearchpython import *
import pandas as pd
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types, TeleBot, ContinueHandling
from telebot.custom_filters import AdvancedCustomFilter
from CallBackFilter import CallbackFilter

from db import DB

db = DB()
db.setup()

API_TOKEN = 'token'

def csv_to_list(file_csv):
    return list(csv.DictReader(open(file_csv, 'r')))


def song_titles(file_csv):
    df = pd.read_csv(file_csv)
    return '\n'.join('\U00002b50 '+str(e) for e in list(df["track"]))

KPOP = csv_to_list('Data/kpop.csv')
ROCK = csv_to_list('Data/rock.csv')
bts = song_titles('Data/bts.csv')
exo = song_titles('Data/exo.csv')
elton = song_titles('Data/elton.csv')
queen = song_titles('Data/queen.csv')

kpops_factory = CallbackData('kpops_id', prefix='kpops')
rocks_factory = CallbackData('rocks_id', prefix='rocks')
bot = TeleBot(API_TOKEN)
markup = types.ReplyKeyboardMarkup(row_width=2)
btn1 = types.KeyboardButton('KPOP')
btn2 = types.KeyboardButton('ROCK')

markup.add(btn1, btn2)
now = datetime.datetime.now()

def greetings():
    greeting = ""
    if 5 <= now.hour < 12:
        greeting = "Good morning"
    elif 12 <= now.hour < 17:
        greeting = "Good afternoon"
    elif 17 <= now.hour <= 23:
        greeting = "Good evening"
    return greeting

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name
    bot.reply_to(message, f"{greetings()} {user} \U00002764,\n"
                          f"Welcome to Songs bot!\n"
                          f"Ask me any songs I will find it for you \n"
                          f"\U0001F4A1 Type /choose + your song\n"
                          f"\U0001F4A1  Type /help if you need my guides")

@bot.message_handler(commands=['help'])
def message_handler(message):
    if db.len_items(message.chat.id) != 0:
        users_song = db.get_items(message.chat.id)
        songs = '\n'.join('\U00002728 ' + str(e) for e in users_song)
        bot.send_message(message.chat.id, f"Here are your favorites :\n"
                                          f"{songs}")

    else:
        bot.send_message(message.chat.id, "You are new here")

    bot.send_message(message.chat.id, "Choose your genre of music?", reply_markup=markup)


@bot.message_handler(commands=['choose'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(message.chat.id, "Here is your song")
    return ContinueHandling()


@bot.message_handler(commands=['choose'])
def start2(message: types.Message):
    song = message.text[7:]
    global chat_id
    chat_id = message.chat.id

    videosSearch = VideosSearch(song, limit=10, language='en', region='US')

    data = videosSearch.result(mode=ResultMode.json)
    d1 = json.loads(data)

    song_id = d1["result"][0]["title"]

    db.add_item(chat_id, message.from_user.first_name, song_id)
    link = d1["result"][0]["link"]
    bot.send_message(chat_id, link)


@bot.message_handler()
def products_command_handler(message: types.Message):
    if message.text == "KPOP":
        bot.send_message(message.chat.id, 'KPOP Artists:', reply_markup=kpop_keyboard())
    elif message.text == "ROCK":
        bot.send_message(message.chat.id, 'ROCK Artists:', reply_markup=rock_keyboard())


@bot.callback_query_handler(func=None, config=kpops_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text
    callback_data1: dict = kpops_factory.parse(callback_data=call.data)

    kpop_id = int(callback_data1['kpops_id'])

    product = KPOP[kpop_id]

    if product['name'] == "BTS":
        text = f"Here are some titles from {product['name']}: {bts}\n"
    elif product['name'] == "EXO":
        text = f"Here are some titles from {product['name']}: {exo}\n"

    bot.send_message(chat_id=call.message.chat.id, text=text)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.callback_query_handler(func=None, config=rocks_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text1
    callback_data2: dict = rocks_factory.parse(callback_data=call.data)
    rock_id = int(callback_data2['rocks_id'])
    product1 = ROCK[rock_id]
    if product1['name'] == "Elton John":
        text1 = f"Here are some titles from {product1['name']}: {elton}\n"

    elif product1['name'] == "Queen":
        text1 = f"Here are some titles from {product1['name']}: {queen}\n"
    bot.send_message(chat_id=call.message.chat.id, text=text1)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


def kpop_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=kpop_artist['name'],
                    callback_data=kpops_factory.new(kpops_id=kpop_artist["id"])
                )
            ]
            for kpop_artist in KPOP
        ]
    )


def rock_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=rock_artist['name'],
                    callback_data=rocks_factory.new(rocks_id=rock_artist["id"])
                )
            ]
            for rock_artist in ROCK
        ]
    )


bot.add_custom_filter(CallbackFilter())

bot.infinity_polling()
