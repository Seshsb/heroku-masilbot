import datetime

import telebot
from telebot import types
from telebot_calendar import CallbackData, Calendar

from db import booking


def inline_category():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = types.InlineKeyboardButton(text='Столы', callback_data='Столы')
    cabins = types.InlineKeyboardButton(text='Кабинки', callback_data='Кабинки')
    markup.add(tables, cabins)

    return markup


def choice_table(reserve_time):
    markup = types.InlineKeyboardMarkup(row_width=2, )
    tables = [types.InlineKeyboardButton(text=str(table[0]),
                                         callback_data=str(table[0])) for table in booking.tables(reserve_time)]
    markup.add(*tables)

    return markup


def choice_cabins(reserve_time):
    markup = types.InlineKeyboardMarkup(row_width=2, )
    tables = [types.InlineKeyboardButton(text=str(table[0]), callback_data=str(table[0])) for table in
              booking.cabins(reserve_time)]
    markup.add(*tables)

    return markup


def booking_confirm():
    markup = types.InlineKeyboardMarkup(row_width=2)
    confirm = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
    cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    markup.add(confirm, cancel)

    return markup


now = datetime.datetime.now()
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
calendar = Calendar()
show_calendar = calendar.create_calendar(
                         name=calendar_1.prefix,
                         year=now.year,
                         month=now.month
)
