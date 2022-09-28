from datetime import datetime
import telebot.apihelper

import dbworker
import config

from telebot_calendar import *
from db import operations
from connections import *
from telebot import types
from flask import request
from functions.handlers import choice_tableid
from keyboards.default import navigation, register
from data.config import START, GET_TABLEID, GET_FIRST_NAME, BOOKING_SUCCESS, GET_PHONE_NUMBER
from keyboards.inline.navigations import inline_category, choice_table, calendar_1, calendar, show_calendar, \
    choice_cabins


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_START.value,
    regexp='Вернуться в меню')
def back_to_menu(message: types.Message):
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


# Бронирование
############################################################################################
@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value,
    regexp='Бронирование')
def text(message):
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING.value)
    bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест',
                     reply_markup=inline_category())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    global seating_category
    if call.data == 'tables':
        seating_category = 1
        bot.send_photo(call.from_user.id, open('./static/booking/tables.jpeg', 'rb'), GET_TABLEID,
                       reply_markup=choice_table())
    elif call.data == 'cabins':
        seating_category = 2
        bot.send_photo(call.from_user.id, open('./static/booking/cabins.jpeg', 'rb'), GET_TABLEID,
                       reply_markup=choice_cabins())
    dbworker.set_states(call.from_user.id, config.States.S_CHOICE_TABLE_ID.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_CHOICE_TABLE_ID.value)
def inline_choice_table(call: types.CallbackQuery):
    global table
    table = operations.table_id(call.data, seating_category)
    bot.send_message(call.from_user.id, 'Отправьте дату и время на которое хотите забронировать \n'
                                        'В формате: дд.мм ЧЧ:ММ. В 24 часовом формате времени', reply_markup=show_calendar)
    dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_DATE.value)
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_date(call: CallbackQuery):
    global date
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    ).strftime('%Y-%m-%d')

    if action == "DAY":
        today_month = datetime.date.today().strftime('%m')
        today_day = datetime.date.today().strftime('%d')
        if int(month) == int(today_month) and int(day) < int(today_day):
            bot.send_message(call.from_user.id, 'выберите правильный день', reply_markup=show_calendar)
            return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)
        bot.send_message(call.from_user.id, 'Пожалуйста, введите время на которое хотите забронировать столик.\n'
                                            'Формат времени ЧЧ:ММ (18:55)')
        dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_TIME.value)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.send_message(call.from_user.id, f"{calendar_1}: Cancellation")


@bot.message_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_TIME.value)
def reserve_time(message: types.Message):
    time = message.text
    if time[:2].isdigit() and time[3:].isdigit():
        if int(time[:2]) <= 23 and int(time[3:]) <= 59:
            global datetime_sql
            datetime_sql = f'{date} {time}'
            bot.send_message(message.from_user.id, 'Пожалйуста, введите количество человек')
            dbworker.set_states(message.from_user.id, config.States.S_BOOKING_HOW_MANY_PEOPLE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_HOW_MANY_PEOPLE.value)
def request_people(message: types.Message):
    global people
    people = message.text
    if people.isdigit():
        bot.send_message(message.from_user.id, GET_PHONE_NUMBER, reply_markup=register.send_contact())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    content_types=['contact'])
def request_contact(message):
    global phone_number
    phone_number = '+' + message.contact.phone_number
    bot.send_message(message.from_user.id, GET_FIRST_NAME)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    regexp=r'\+998[0-9]{9,9}$')
def phone(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, GET_FIRST_NAME)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_FIRSTNAME.value)
def get_first_name(message):
    global first_name
    first_name = message.text
    operations.start_booking(message.from_user.id, table, datetime_sql, phone_number, first_name, people)
    bot.send_message(message.from_user.id, BOOKING_SUCCESS, reply_markup=navigation.back_to_menu())
    dbworker.set_states(message.from_user.id, config.States.S_START.value)


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
