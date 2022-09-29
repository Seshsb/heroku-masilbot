from telebot import types


def booking_or_delivery():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Бронирование')
    button2 = types.KeyboardButton('Доставка')
    markup.add(button1, button2)

    return markup


def back_to_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Вернуться в меню')
    markup.add(button1)

    return markup
