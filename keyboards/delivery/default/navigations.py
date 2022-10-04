from telebot import types
from db import deliveryDB


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    basket = types.KeyboardButton('Корзина')
    markup.add(*[category[0] for category in deliveryDB.get_categories()])
    markup.add(basket)

    return markup


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    basket = types.KeyboardButton('Корзина')
    markup.add(*[dish[0] for dish in deliveryDB.get_dishes(cat_id)])
    markup.add(basket)

    return markup


def numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    basket = types.KeyboardButton('Корзина')
    markup.add(*[str(num) for num in range(1, 10)])
    markup.add(basket)

    return markup
