import datetime

import telebot
from telebot import types

from data.config import trans
from telebot_calendar import CallbackData, Calendar, RUSSIAN_LANGUAGE

from db import bookingDB


def inline_category(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = types.InlineKeyboardButton(text=trans['booking'][f'TABLES_{lang}'],
                                        callback_data=trans['booking'][f'TABLES_{lang}'])
    cabins = types.InlineKeyboardButton(text=trans['booking'][f'CABINS_{lang}'],
                                        callback_data=trans['booking'][f'CABINS_{lang}'])
    cancel = types.InlineKeyboardButton(text=trans['general'][f'CANCEL_{lang}'], callback_data='cancel')
    markup.add(tables, cabins)
    markup.add(cancel)

    return markup


def choice_table(reserve_time, lang):
    markup = types.InlineKeyboardMarkup(row_width=2, )
    tables = [types.InlineKeyboardButton(text=str(table[0]),
                                         callback_data=str(table[0])) for table in bookingDB.tables(reserve_time)]
    cancel = types.InlineKeyboardButton(text=trans['general'][f'CANCEL_{lang}'], callback_data='cancel')
    markup.add(*tables)
    markup.add(cancel)

    return markup


def choice_cabins(reserve_time, lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = [types.InlineKeyboardButton(text=f'{table[0]} '
                                              f'({trans["booking"][f"PEOPLE_{lang}"]}{table[1]}~{table[2]})',
                                         callback_data=str(table[0])) for table in bookingDB.cabins(reserve_time)]
    cancel = types.InlineKeyboardButton(text=trans['general'][f'CANCEL_{lang}'], callback_data='cancel')
    markup.add(*tables)
    markup.add(cancel)

    return markup


def booking_confirm(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    confirm = types.InlineKeyboardButton(trans['general'][f'ACCEPT_{lang}'], callback_data='confirm')
    cancel = types.InlineKeyboardButton(trans['general'][f'CANCEL_{lang}'], callback_data='cancel')
    markup.add(confirm, cancel)

    return markup


now = datetime.datetime.now()
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
calendar = Calendar(language=RUSSIAN_LANGUAGE)
show_calendar = calendar.create_calendar(
                         name=calendar_1.prefix,
                         year=now.year,
                         month=now.month)
