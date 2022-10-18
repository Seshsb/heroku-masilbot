from telebot import types

from data.config import trans


def payment_method(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    cash = types.InlineKeyboardButton(text=trans['delivery'][f'DELIVERY_CASH_METHOD_{lang}'], callback_data='cash')
    payme = types.InlineKeyboardButton(text=trans['delivery'][f'DELIVERY_PAYME_METHOD_{lang}'], callback_data='payme')
    markup.add(cash, payme)

    return markup


def accepting_order(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    accept = types.InlineKeyboardButton(text=trans['general'][f'ACCEPT_{lang}'], callback_data='accept')
    cancel = types.InlineKeyboardButton(text=trans['general'][f'CANCEL_{lang}'], callback_data='cancel')
    markup.add(accept, cancel)

    return markup
