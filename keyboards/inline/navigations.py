import telebot
from telebot import types


def inline_category():
    markup = types.InlineKeyboardMarkup(row_width=2)
    tables = types.InlineKeyboardButton(text='Столы', callback_data='tables')
    cabins = types.InlineKeyboardButton(text='Кабинки', callback_data='cabins')
    markup.add(tables, cabins)

    return markup