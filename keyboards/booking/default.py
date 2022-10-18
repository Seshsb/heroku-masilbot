from telebot import types

from data.config import trans


def base(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(back, main_page)

    return markup


def quantity_people(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(*[str(num) for num in range(1, 10)])
    markup.add(back)
    markup.add(main_page)

    return markup