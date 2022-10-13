from telebot import types

def payment_method():
    markup = types.InlineKeyboardMarkup(row_width=2)
    cash = types.InlineKeyboardButton(text='Наличными 💵', callback_data='cash')
    payme = types.InlineKeyboardButton(text='PayMe 💵', callback_data='payme')
    markup.add(cash, payme)

    return markup


def accepting_order():
    markup = types.InlineKeyboardMarkup(row_width=2)
    accept = types.InlineKeyboardButton(text='Подтвердить', callback_data='accept')
    cancel = types.InlineKeyboardButton(text='Отменить', callback_data='cancel')
    markup.add(accept, cancel)

    return markup
