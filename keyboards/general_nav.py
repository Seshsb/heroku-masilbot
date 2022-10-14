from telebot import types


def booking_or_delivery():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Бронирование')
    button2 = types.KeyboardButton('Доставка')
    markup.add(button1, button2)

    return markup


def main_page():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(button1)

    return markup


def send_contact():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    button = types.KeyboardButton('Отправить контакт', request_contact=True)
    markup.add(button)

    return markup