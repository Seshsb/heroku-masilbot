from telebot import types
from data.config import trans


def choice_lang():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton(trans['general']['RUSSIAN'])
    button2 = types.KeyboardButton(trans['general']['KOREAN'])
    markup.add(button1, button2)

    return markup


def main_page(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    booking = types.KeyboardButton(trans['general'][f'BOOKING_{lang}'])
    delivery = types.KeyboardButton(trans['general'][f'DELIVERY_{lang}'])
    change_lang = types.KeyboardButton(trans['general'][f'CHANGE_LANG_{lang}'])
    markup.add(booking, delivery, change_lang)

    return markup


def back_to_main_page(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(button1)

    return markup


def send_contact(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    button = types.KeyboardButton(trans['general'][f'SEND_CONTACT_{lang}'], request_contact=True)
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(button)
    markup.add(back, main_page)

    return markup


def error():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    markup.add(types.KeyboardButton('/start'))

    return markup