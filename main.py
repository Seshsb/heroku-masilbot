import telebot

from connections import *
from telebot import types
from flask import Flask, request
from functions.handlers import reserve_time, get_table_id
from keyboards.default import navigation, register
from data.config import START, GET_TABLEID
from keyboards.inline.navigations import inline_category


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    return bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


@bot.message_handler(regexp='Бронирование')
def booking(message):
    bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест',
                     reply_markup=inline_category())


@bot.message_handler(func=lambda message: reserve_time(message) == True, content_types=['contact'])
def request_contact(message):
    phone_number = '+' + message.contact.phone_number
    bot.send_message(message.from_user.id, GET_TABLEID)
    bot.register_next_step_handler(message, get_table_id, phone_number)


@bot.message_handler(regexp=r'\+998+')
def phone(message):
    bot.send_message(message.from_user.id, 'ok')


@bot.callback_query_handler(func=lambda call: True)
def inline_seating_category(call: types.CallbackQuery):
    if call.data == 'tables':
        bot.send_message(call.from_user.id, 'Отправьте дату и время на которое хотите забронировать \n'
                                            'В формате: дд.мм ЧЧ:ММ. В 24 часовом формате времени')
        bot.register_next_step_handler(call.message, reserve_time)


@server.route(f'/{BOT_TOKEN}', methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('APP_URL') + BOT_TOKEN)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
