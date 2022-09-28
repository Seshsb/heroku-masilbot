from datetime import datetime

import dbworker
import config

from telebot_calendar import *
from db import operations
from connections import *
from telebot import types
from flask import request
from keyboards.default import navigation, register
from data.config import *
from keyboards.inline.navigations import *


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
    bot.send_message(message.from_user.id, REQUEST_CATEGORY,
                     reply_markup=inline_category())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    global seating_category
    if call.data == 'Столы':
        seating_category = 1
        bot.send_photo(call.from_user.id, open('./static/booking/tables.jpeg', 'rb'), GET_TABLEID,
                       reply_markup=choice_table())
    elif call.data == 'Кабинки':
        seating_category = 2
        bot.send_photo(call.from_user.id, open('./static/booking/cabins.jpg', 'rb'), GET_TABLEID,
                       reply_markup=choice_cabins())
    dbworker.set_states(call.from_user.id, config.States.S_CHOICE_SEATING_ID.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_CHOICE_SEATING_ID.value)
def inline_choice_table(call: types.CallbackQuery):
    global table_id
    global table
    table = call.data
    table_id = operations.table_id(table, seating_category)
    bot.send_message(call.from_user.id, REQUEST_DATE, reply_markup=show_calendar)
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
            bot.send_message(call.from_user.id, UNSUCCESS_DATE, reply_markup=show_calendar)
            return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)
        bot.send_message(call.from_user.id, REQUEST_TIME)
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
            bot.send_message(message.from_user.id, REQUEST_PEOPLE)
            dbworker.set_states(message.from_user.id, config.States.S_BOOKING_HOW_MANY_PEOPLE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_BOOKING_HOW_MANY_PEOPLE.value)
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
    bot.send_message(message.from_user.id, 'Детали бронирования:\n\n'
                                           f'Имя: {first_name}\n'
                                           f'Телефон: {phone_number[1:]}\n'
                                           f'Дата и время: {datetime_sql.replace("-", ".")}\n'
                                           f'Посадочное место: {operations.seating_category(seating_category)[0]}\n'
                                           f'Стол: {table}\n'
                                           f'Количество человек: {people}', reply_markup=booking_confirm())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_CONFIRMATION.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_CONFIRMATION.value)
def inline_confirmation(call):
    if call.data == 'confirm':
        operations.start_booking(call.from_user.id, table_id, datetime_sql, phone_number, first_name, people)
        bot.send_message(call.from_user.id, BOOKING_CONFIRMED, reply_markup=navigation.back_to_menu())
        dbworker.set_states(call.from_user.id, config.States.S_START.value)
    else:
        bot.send_message(call.from_user.id, BOOKING_CANCELED, reply_markup=navigation.back_to_menu())
        dbworker.set_states(call.from_user.id, config.States.S_START.value)


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
