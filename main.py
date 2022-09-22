import os
import telebot
import logging

from telebot import types
from flask import Flask, request
from os.path import join, dirname
from dotenv import load_dotenv
from db import operations

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.from_user.id, 'hi')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton('Отправить контакт', request_contact=True)
    markup.add(button)
    text = 'Пройди регистрацию, нажми на кнопку и отправь номер телефона или напиши его в формате (+998*********)'

    bot.send_message(message.from_user.id, text, reply_markup=markup)

# @bot.message_handler(commands=['contact'])
# def register(message):
#     id = message.from_user.id
#     if operations.cursor.execute('SELECT * FROM users WHERE phone_number=%s ;', (message.from_user.phone_number)):
#         text = ''
#     text = 'Отлично, вы успешно зарегистрированы'

@server.route(f'/{BOT_TOKEN}', methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('APP_URL') + BOT_TOKEN)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))