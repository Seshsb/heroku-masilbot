from telebot import types

from db import deliveryDB
q=[food[0] for food in deliveryDB.foods_name(275755142)]
print(q)

def inline_order(user_id):
    markup = types.InlineKeyboardMarkup()
    cancel = [types.InlineKeyboardButton(text=f'❌ Удалить {food[0]}', callback_data=f'{food[0]} delete') for food in deliveryDB.foods_name(int(user_id))]
    markup.add(types.InlineKeyboardButton('Оформить заказ', callback_data='order'))
    markup.add(*cancel)
    return markup