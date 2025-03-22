import telebot
from telebot import types
from dotenv import load_dotenv
from translate import Translator
import requests
import json
import os

with open("locale.json", "r", encoding="utf-8") as file: locales = json.load(file)
ukr = locales["ukr"]
eng = locales["eng"]
translator = Translator(to_lang="uk")
load_dotenv()
TOKEN = os.getenv("api")
bot = telebot.TeleBot(TOKEN)

def getfact():
    response = requests.get("https://catfact.ninja/fact").json()
    return response["fact"]

def getfactua():
    fact = getfact()
    return translator.translate(fact)

@bot.message_handler(commands=['start'])
def start(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = types.KeyboardButton(ukr["button1"])
  item2 = types.KeyboardButton(ukr["button2"])
  markup.add(item1, item2)
  bot.send_message(message.chat.id, "Hello!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == ukr["button1"])
def button1_action(message):
    fact = getfact()
    factua = getfactua()
    bot.send_message(message.chat.id, factua)

@bot.message_handler(func=lambda message: message.text == ukr["button2"])
def button2_action(message):
    bot.send_message(message.chat.id, "В розробці...")

if __name__ == "__main__":
    bot.infinity_polling()