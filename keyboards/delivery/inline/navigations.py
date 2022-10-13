from telebot import types

def payment_method():
    markup = types.InlineKeyboardMarkup(row_width=2)
    cash = types.InlineKeyboardButton('Наличными 💵', 'cash')
    payme = types.InlineKeyboardButton('PayMe 💵', 'payme')
    markup.add(cash, payme)

    return markup


def accepting_order():
    markup = types.InlineKeyboardMarkup(row_width=2)
    accept = types.InlineKeyboardButton('Подтвердить', 'accept')
    cancel = types.InlineKeyboardButton('Отменить', 'cancel')
    markup.add(accept, cancel)

    return markup
