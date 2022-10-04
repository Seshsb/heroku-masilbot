from telebot import types
from db import delivery


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
    markup.add(*[category[0] for category in delivery.get_categories()])


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
    markup.add(*[dish[0] for dish in delivery.get_dishes(cat_id)])