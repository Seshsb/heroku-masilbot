from telebot import types

from db import deliveryDB


def inline_order(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Оформить заказ', callback_data='order'),
               *[types.InlineKeyboardButton(f'❌ {food[0]}', callback_data=f'{food[0]} delete') for food in deliveryDB.show_basket(user_id)])
    return markup