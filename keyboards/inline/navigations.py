import datetime

import telebot
from telebot import types
from telebot_calendar import CallbackData, Calendar

from db import operations


def inline_category():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = types.InlineKeyboardButton(text='Столы', callback_data='tables')
    cabins = types.InlineKeyboardButton(text='Кабинки', callback_data='cabins')
    markup.add(tables, cabins)

    return markup


def choice_table():
    markup = types.InlineKeyboardMarkup(row_width=2, )
    tables = [types.InlineKeyboardButton(text=str(table[0]), callback_data=str(table[0])) for table in operations.tables()]
    markup.add(*tables)

    return markup

now = datetime.datetime.now()
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
calendar = Calendar()
show_calendar = calendar.create_calendar(
                         name=calendar_1.prefix,
                         year=now.year,
                         month=now.month
)

# def start_time():
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     left_arrow = types.InlineKeyboardButton('<', callback_data='left')
#     right_arrow = types.InlineKeyboardButton('>', callback_data='right')
#     time_start = types.InlineKeyboardButton('00:00', callback_data='time')
#     submit = types.InlineKeyboardButton('Дальше', callback_data='submit')
#     markup.add(*[left_arrow, time_start, right_arrow, submit])
#
#     return markup