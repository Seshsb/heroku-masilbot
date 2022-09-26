from datetime import datetime

import telebot.apihelper

import dbworker
import config

from db import operations
from connections import *
from telebot import types
from flask import request
from functions.handlers import choice_tableid
from keyboards.default import navigation, register
from data.config import START, GET_TABLEID, GET_FIRST_NAME, BOOKING_SUCCESS, GET_PHONE_NUMBER
from keyboards.inline.navigations import inline_category, choice_table


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_START.value, regexp='Вернуться в меню')
def back_to_menu(message: types.Message):
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())

# Бронирование
############################################################################################
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value, regexp='Бронирование')
def text(message):
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING.value)
    bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест',
                    reply_markup=inline_category())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_START_AT.value)
def reserve_time(message: types.Message):
    time = message.text
    global time_sql
    time_sql = f'{str(datetime.today().year)}-{time[3:5]}-{time[:2]} {time[6:]}'
    bot.send_message(message.from_user.id, GET_PHONE_NUMBER, reply_markup=register.send_contact())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value, content_types=['contact'])
def request_contact(message):
    global phone_number
    phone_number = '+' + message.contact.phone_number
    bot.send_message(message.from_user.id, GET_FIRST_NAME)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value, regexp=r'\+998[0-9]{9,9}$')
def phone(message):
    global phone_number
    phone_number = message.text
    bot.send_photo(message.from_user.id, open('./static/booking/tables.jpeg', 'rb'), GET_TABLEID,
                   reply_markup=choice_table())
    dbworker.set_states(message.from_user.id, config.States.S_CHOICE_TABLE_ID.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_FIRSTNAME.value)
def get_first_name(message):
    global first_name
    first_name = message.text
    bot.send_photo(message.from_user.id, open('./static/booking/tables.jpeg', 'rb'), GET_TABLEID,
                   reply_markup=choice_table())
    dbworker.set_states(message.from_user.id, config.States.S_CHOICE_TABLE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_CHOICE_TABLE_ID.value)
def get_table_id(message: types.Message):
    table_id = message.text
    operations.start_booking(message.from_user.id, table_id, time_sql, phone_number, first_name)
    bot.send_message(message.from_user.id, BOOKING_SUCCESS, reply_markup=navigation.back_to_menu())
    dbworker.set_states(message.from_user.id, config.States.S_START.value)



@bot.callback_query_handler(func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    if call.data == 'tables':
        dbworker.set_states(call.from_user.id, config.States.S_CHOICE_TABLE.value)
        bot.send_message(call.from_user.id, 'Отправьте дату и время на которое хотите забронировать \n'
                                            'В формате: дд.мм ЧЧ:ММ. В 24 часовом формате времени')
        dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_AT.value)
    elif call.data == 'table1':
        bot.send_message(call.message.from_user.id, call)


############################################################################################


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
