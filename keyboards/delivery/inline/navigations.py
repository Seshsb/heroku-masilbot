from telebot import types

from db import deliveryDB
q=[food[0] for food in deliveryDB.show_basket(275755142)]
print(q)
def inline_order(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    cancel = [types.InlineKeyboardButton(f'{food[0]}', callback_data=f'{food[0]} delete') for food in deliveryDB.show_basket(user_id)]
    markup.add(types.InlineKeyboardButton('Оформить заказ', callback_data='order'), *cancel)
    return markup