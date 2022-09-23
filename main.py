import os
import telebot
import logging

from telebot import types
from flask import Flask, request
from os.path import join, dirname
from dotenv import load_dotenv
from db import operations
from functions.handlers import reserve_time
from keyboards.default import navigation, register
from data.config import START
from keyboards.inline.navigations import inline_category

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
    # if operations.user_exist(message.from_user.id):
    #     return bot.send_message(message.from_user.id, 'Выберите действие',
    #                             reply_markup=navigation.booking_or_delivery())
    return bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


@bot.message_handler(content_types=['contact', 'text'])
def text_contacts(message: types.Message):
    if message.text == 'Бронирование':
        bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест', reply_markup=inline_category())

    # booking(message, bot)
    bot.send_message(message.from_user.id, str(message))



@bot.callback_query_handler(func=lambda call: True)
def inline_seating_category(message: types.Message, call: types.CallbackQuery):
    if call.data == 'Столы':
        bot.send_message(call.from_user.id, 'Отправьте дату и время на которое хотите забронировать \n'
                                            'В формате: дд.мм ЧЧ:ММ. В 24 часовом формате времени')
        bot.register_next_step_handler(message,  reserve_time)


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