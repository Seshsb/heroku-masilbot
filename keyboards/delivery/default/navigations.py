from telebot import types
from db import deliveryDB


def food_categoriesRu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    markup.add(basket)
    markup.add(*[category[0] for category in deliveryDB.get_categories()])
    markup.add(back)

    return markup


def dishesRu(cat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(basket)
    markup.add(*[dish[0] for dish in deliveryDB.get_dishes(cat_id)])
    markup.add(back)
    markup.add(main_page)

    return markup


def numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    basket = types.KeyboardButton('Корзина')
    back = types.KeyboardButton('Назад')
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(basket)
    markup.add(*[str(num) for num in range(1, 10)])
    markup.add(back)
    markup.add(main_page)

    return markup


def order(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    cancel = [types.KeyboardButton(text=f'❌ Удалить {food[0]}') for food in deliveryDB.foods_name(int(user_id))]
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(types.KeyboardButton('Оформить заказ'))
    markup.add(*cancel)
    markup.add(main_page)
    return markup


def send_location():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True, one_time_keyboard=True)
    location = types.KeyboardButton('Поделиться локацией 🌐',request_location=True)
    takeaway = types.KeyboardButton('На вынос 🏃🏻‍♂️')
    main_page = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(takeaway, location, main_page)

    return markup