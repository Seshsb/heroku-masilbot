from telebot import types

from data.config import trans
from db import deliveryDB


def food_categoriesRu(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    basket = types.KeyboardButton(trans['delivery'][f'BASKET_{lang}'])
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    markup.add(basket)
    markup.add(*[category[0] for category in deliveryDB.get_categories(lang)])
    markup.add(back)

    return markup


def dishesRu(cat_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    basket = types.KeyboardButton(trans['delivery'][f'BASKET_{lang}'])
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(basket)
    markup.add(*[dish[0] for dish in deliveryDB.get_dishes(cat_id, lang)])
    markup.add(back)
    markup.add(main_page)

    return markup


def numbers(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    basket = types.KeyboardButton(trans['delivery'][f'BASKET_{lang}'])
    back = types.KeyboardButton(trans['general'][f'BACK_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(basket)
    markup.add(*[str(num) for num in range(1, 10)])
    markup.add(back)
    markup.add(main_page)

    return markup


def order(user_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    cancel = [types.KeyboardButton(text=trans['delivery'][f'DELETE_{lang}']
                                   .format(food[0])) for food in deliveryDB.foods_name(int(user_id), lang)]
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(types.KeyboardButton(trans['delivery'][f'ORDER_{lang}']))
    markup.add(*cancel)
    markup.add(main_page)
    return markup


def send_location(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True, one_time_keyboard=True)
    location = types.KeyboardButton(trans['delivery'][f'SEND_LOCATION_{lang}'],request_location=True)
    takeaway = types.KeyboardButton(trans['delivery'][f'TAKEAWAY_{lang}'])
    main_page = types.KeyboardButton(trans['general'][f'BACK_TO_MAIN_PAGE_{lang}'])
    markup.add(takeaway, location, main_page)

    return markup