import telebot
from telebot import types
from db import operations


def inline_category():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = types.InlineKeyboardButton(text='Столы', callback_data='tables')
    cabins = types.InlineKeyboardButton(text='Кабинки', callback_data='cabins')
    markup.add(tables, cabins)

    return markup


def choice_table():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = [str(table[0]) for table in operations.tables()]
    markup.add(*tables)

    return markup