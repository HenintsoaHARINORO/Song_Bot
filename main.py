import csv
import json
import datetime
import random

import constant
import pandas as pd
from youtubesearchpython import *
from telebot import TeleBot, types, ContinueHandling
from telebot.callback_data import CallbackData

import dbAlchemy
from CallBackFilter import CallBackFilter


def csv_to_list(file_csv):
    return random.sample(list(csv.DictReader(open(file_csv, 'r'))), constant.RANDOM)


# function that fetches the title of songs from csv files
def song_titles(file_csv):
    df = pd.read_csv(file_csv)
    return '\n'.join(constant.SPARKLE_EMOJI + str(e) for e in random.sample(list(df["track"]),constant.RANDOM))


# Take 2 random elements from the file to be suggested to the user
KPOP = csv_to_list('Data/kpop.csv')
ROCK = csv_to_list('Data/rock.csv')
bts = song_titles('Data/bts.csv')
exo = song_titles('Data/exo.csv')
elton = song_titles('Data/elton.csv')
queen = song_titles('Data/queen.csv')

kpops_factory = CallbackData('kpops_id', prefix='kpops')
rocks_factory = CallbackData('rocks_id', prefix='rocks')
bot = TeleBot(constant.API_TOKEN)
markup = types.ReplyKeyboardMarkup(row_width=2)
btn1 = types.KeyboardButton('KPOP')
btn2 = types.KeyboardButton('ROCK')

markup.add(btn1, btn2)
now = datetime.datetime.now()


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
    bot.send_message(message.chat.id, "Here is your song")
    return ContinueHandling()


@bot.message_handler(commands=['choose'])
def start2(message: types.Message):
    song = message.text.split(' ', 1)[1]  # get the title /or singer after the command /choose
    videos_search = VideosSearch(song, limit=10, language='en', region='US')
    data = videos_search.result(mode=ResultMode.json)
    d1 = json.loads(data)
    song_id = d1["result"][0]["title"]  # extract the title and singer from json
    dbAlchemy.add_item(message.chat.id, message.from_user.first_name, song_id)
    link = d1["result"][0]["link"]  # extract the link
    bot.send_message(message.chat.id, link)


# suggests to the user by genre of music
@bot.message_handler()
def products_command_handler(message: types.Message):
    if message.text == "KPOP":
        bot.send_message(message.chat.id, 'KPOP bands:', reply_markup=kpop_keyboard())
    elif message.text == "ROCK":
        bot.send_message(message.chat.id, 'ROCK singers:', reply_markup=rock_keyboard())


@bot.callback_query_handler(func=None, config=kpops_factory.filter())
def singers_callback(call: types.CallbackQuery):
    text = ""
    callback_data: dict = kpops_factory.parse(callback_data=call.data)
    kpop_id = int(callback_data['kpops_id'])
    singer = KPOP[kpop_id]
    if singer['name'] == "BTS":
        text = f"Here are some titles from {singer['name']}:\n {bts}\n"
    elif singer['name'] == "EXO":
        text = f"Here are some titles from {singer['name']}:\n {exo}\n"

    bot.send_message(chat_id=call.message.chat.id, text=text)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


@bot.callback_query_handler(func=None, config=rocks_factory.filter())
def singers_callback(call: types.CallbackQuery):
    text1 = ""
    callback_data2: dict = rocks_factory.parse(callback_data=call.data)
    rock_id = int(callback_data2['rocks_id'])
    singer = ROCK[rock_id]
    if singer['name'] == "Elton John":
        text1 = f"Here are some titles from {singer['name']}:\n {elton}\n"

    elif singer['name'] == "Queen":
        text1 = f"Here are some titles from {singer['name']}: \n {queen}\n"
    bot.send_message(chat_id=call.message.chat.id, text=text1)
    bot.send_message(call.message.chat.id, "Now you can choose from this list with /choose + the title")


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


bot.add_custom_filter(CallBackFilter())

bot.infinity_polling()
