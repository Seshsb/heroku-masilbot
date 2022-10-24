from telebot import types

from data.config import trans


def payment_method(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    cash = types.InlineKeyboardButton(text=trans['delivery'][f'DELIVERY_CASH_METHOD_{lang}'], callback_data='cash')
    payme = types.InlineKeyboardButton(text=trans['delivery'][f'DELIVERY_PAYME_METHOD_{lang}'], callback_data='payme')
    markup.add(cash, payme)

    return markup


def accepting_order(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    accept = types.KeyboardButton(text=trans['general'][f'ACCEPT_{lang}'])
    cancel = types.KeyboardButton(text=trans['general'][f'CANCEL_{lang}'])
    markup.add(accept, cancel)

    return markup
