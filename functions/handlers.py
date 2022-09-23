import datetime
from db import operations
from telebot import types

def reserve_time(message: types.Message, bot):
    time = message.text
    time_sql = time[:2] + '-' + time[3:5] + ' ' + time[6:]
    bot.send_message(message.from_user.id, time_sql)


