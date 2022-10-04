from telebot import types

def back_to_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Вернуться на главную страницу')
    markup.add(button1)

    return markup