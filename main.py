import os
import telebot
import logging

from telebot import types
from flask import Flask, request
from os.path import join, dirname
from dotenv import load_dotenv
from db import operations
from functions.register import register
from keyboards.default import navigation, register
from data.config import START

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.from_user.id, str(message))
    if operations.user_exist(message.from_user.id):
        return bot.send_message(message.from_user.id, 'Выберите действие',
                                reply_markup=navigation.booking_or_delivery())
    return bot.send_message(message.chat.id, START, reply_markup=register.send_contact())


@bot.message_handler(content_types=['contact', 'text'])
def text_contacts(message: types.Message):
    register(message, bot)
    bot.send_message(message.from_user.id, str(message))


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