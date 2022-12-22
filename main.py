import csv
import json

from youtubesearchpython import *
import pandas as pd
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types, TeleBot, ContinueHandling
from telebot.custom_filters import AdvancedCustomFilter


from db import DBot

db = DBot()
db.setup()

API_TOKEN = '<token>'
myFile = open('./Data/kpop.csv', 'r')
reader = csv.DictReader(myFile)
myList = list(reader)
PRODUCTS = myList
df = pd.read_csv('./Data/bts.csv')
a = list(df["track"])
b = '\n'.join(str(e) for e in a)

bot = TeleBot(API_TOKEN)
products_factory = CallbackData('product_id', prefix='products')


def products_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=product['name'],
                    callback_data=products_factory.new(product_id=product["id"])
                )
            ]
            for product in PRODUCTS
        ]
    )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    user = message.from_user.first_name
    db.add_user(chat_id,user)
    bot.reply_to(message, f"Hello {user},Welcome to Songs bot!\nType /choose + your song or /help ")


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('KPOP')
itembtn2 = types.KeyboardButton('ROCK')
itembtn3 = types.KeyboardButton('JAZZ')
markup.add(itembtn1, itembtn2, itembtn3)


@bot.message_handler(commands=['help'])
def message_handler(message):
    global chat_id
    chat_id = message.chat.id
    if len(db.get_items(chat_id)) != 0:
        bot.send_message(message.chat.id, f"Here are your favorites genre: {db.get_items(chat_id)}")
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

    videosSearch = VideosSearch(message.text[7:], limit=10, language='en', region='US')

    data = videosSearch.result(mode=ResultMode.json)
    d1 = json.loads(data)

    id_song = d1["result"][0]["title"]
    artist,title = list(id_song.split('-'))

    db.add_item(chat_id, message.from_user.first_name, artist,title)
    link = d1["result"][0]["link"]
    bot.send_message(chat_id, link)


@bot.message_handler()
def products_command_handler(message: types.Message):
    if message.text == "KPOP":

        bot.send_message(message.chat.id, 'Products:', reply_markup=products_keyboard())


@bot.callback_query_handler(func=None, config=products_factory.filter())
def products_callback(call: types.CallbackQuery):
    global text
    callback_data: dict = products_factory.parse(callback_data=call.data)
    product_id = int(callback_data['product_id'])
    product = PRODUCTS[product_id]
    if product['name'] == "BTS":
        text = f"Here are some titles: {b}\n"
    bot.send_message(chat_id=call.message.chat.id, text=text)


bot.add_custom_filter(ProductsCallbackFilter())

bot.infinity_polling()


