from telebot import types
from db import delivery


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[category[0] for category in delivery.get_categories()])

    return markup


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[dish[0] for dish in delivery.get_dishes(cat_id[0])])

    return markup
