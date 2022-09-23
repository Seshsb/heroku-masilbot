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
        bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест',
                         reply_markup=inline_category())

    # booking(message, bot)
    bot.send_message(message.from_user.id, str(message))


@bot.message_handler(func=reserve_time, content_types=['text', 'contact'])
def test(message):
    if message.text[:4] == '+998':
        if message.text[1:].isdigit() and len(message.text) == 13:
            phone_number = message.text
            operations.create_user(message.from_user.id, phone_number)
            return bot.send_message(message.from_user.id, '1')
        return bot.send_message(message.from_user.id, '0')

    elif message.text[1:].isdigit and message.text[:4] != '+998':
        return bot.send_message(message.from_user.id, '1')

    elif message.content_type == 'contact':
        if message.contact.phone_number[:3] == '998' and len(message.contact.phone_number) == 12:
            phone_number = '+' + message.contact.phone_number
        elif message.contact.phone_number[0:4] == '+998' and len(message.contact.phone_number) == 12:
            phone_number = message.contact.phone_number
        else:
            return bot.send_message(message.from_user.id, '0')

        operations.create_user(message.from_user.id, phone_number)
        return bot.send_message(message.from_user.id, '1')


@bot.callback_query_handler(func=lambda call: True)
def inline_seating_category(call: types.CallbackQuery):
    if call.data == 'tables':
        bot.send_message(call.from_user.id, 'Отправьте дату и время на которое хотите забронировать \n'
                                            'В формате: дд.мм ЧЧ:ММ. В 24 часовом формате времени')
        bot.register_next_step_handler(call.message, reserve_time, bot)


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