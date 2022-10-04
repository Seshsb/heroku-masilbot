from telebot import types
from db import deliveryDB


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[category[0] for category in deliveryDB.get_categories()])

    return markup


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[dish[0] for dish in deliveryDB.get_dishes(cat_id)])

    return markup


def numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[str(num) for num in range(0, 10)])

    return markup