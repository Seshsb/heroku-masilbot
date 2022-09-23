import datetime
from db import operations
from telebot import types
from data.config import GET_PHONE_NUMBER, FORMAT_NUMBER_INVALID


def reserve_time(message: types.Message, bot):
    time = message.text
    time_sql = time[:2] + '-' + time[3:5] + ' ' + time[6:]
    bot.send_message(message, GET_PHONE_NUMBER)
    bot.register_next_step_handler(message, get_phone_number, time)


def get_phone_number(message: types.Message, bot, time, phone_number):
    if message.content_type == 'text':
        if message.text[1:].isdigit() and len(message.text) == 13:
            phone_number = message.text
            operations.create_user(message.from_user.id, phone_number)
            bot.send_message(message, 'Напишите свое имя')
        else:
            bot.send_message(message, FORMAT_NUMBER_INVALID)
            reserve_time(message, bot)
