from telebot import types


def send_contact():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton('Отправить контакт', request_contact=True)
    markup.add(button)

    return markup
