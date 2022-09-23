import datetime
from db import operations
from main import bot
from telebot import types
from data.config import GET_PHONE_NUMBER, FORMAT_NUMBER_INVALID


def reserve_time(message: types.Message):
    time = message.text
    time_sql = time[:2] + '-' + time[3:5] + ' ' + time[6:]
    bot.send_message(message, GET_PHONE_NUMBER)
    bot.register_next_step_handler(message, get_phone_number, time)


def get_phone_number(message: types.Message, time, phone_number):
    return message.text[:4] == '+998'


@bot.message_handler(func=get_phone_number, content_types=['text', 'contact'])
def test(message):
    bot.send_message(message.from_user.id, 'test')