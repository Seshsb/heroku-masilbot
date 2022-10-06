from telebot import types
from db import deliveryDB


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    markup.add(*[category[0] for category in deliveryDB.get_categories()])
    markup.add(basket, back)

    return markup


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(*[dish[0] for dish in deliveryDB.get_dishes(cat_id)])
    markup.add(basket, back, main_page)

    return markup


def numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(*[str(num) for num in range(1, 10)])
    markup.add(basket, back, main_page)

    return markup


def order(user_id):
    markup = types.InlineKeyboardMarkup()
    cancel = [types.InlineKeyboardButton(text=f'❌ Удалить {food[0]}', callback_data=f'{food[0]} delete') for food in deliveryDB.foods_name(int(user_id))]
    markup.add(types.InlineKeyboardButton('Оформить заказ', callback_data='order'), *cancel)
    return markup
