import traceback
import telebot.apihelper
import telebot.storage
from telebot.types import CallbackQuery

import dbworker
import config

from datetime import timedelta
from db import DataBase
from connections import *
from flask import request
from keyboards import general_nav
from keyboards.delivery.default.navigations import *
from keyboards.delivery.inline.navigations import *
from keyboards.booking.inline.navigations import *
from keyboards.booking.default import *
from functions.handlers import *

user_dict = dict()

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        if DataBase.get_user(message.from_user.id):
            lang = DataBase.get_user_lang(message.from_user.id)[0]
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_CHOICE_LANGUAGE.value)
def action_choice(message: types.Message):
    lang = ''
    try:
        if message.text == 'Русский 🇷🇺':
            lang = trans['general']['LANGUAGE_RU']
        elif message.text == '한국어 🇰🇷':
            lang = trans['general']['LANGUAGE_KO']

        if DataBase.get_user(message.from_user.id):
            DataBase.change_lang(message.from_user.id, lang)
            bot.send_message(message.from_user.id, trans['general'][f'CHANGE_LANG_SUCCESS_{lang}'])
        else:
            DataBase.register(message.from_user.id, lang)
        bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                         reply_markup=general_nav.main_page(lang))
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


def end(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value)
def booking_or_delivery(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BOOKING_{lang}']:
            booking(message)
        elif message.text == trans['general'][f'DELIVERY_{lang}']:
            delivery(message)
        elif message.text == trans['general'][f'CHANGE_LANG_{lang}']:
            bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                             reply_markup=general_nav.choice_lang())
            dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


# Бронирование
############################################################################################
def booking(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)

    try:
        bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_DATE_{lang}'],
                         reply_markup=show_calendar)
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_DATE.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_DATE.value)
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_date(call: CallbackQuery):
    lang = DataBase.get_user_lang(call.from_user.id)[0]
    if not lang:
        bot.send_message(call.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(call.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        name, action, year, month, day = call.data.split(calendar_1.sep)

        if action == "DAY":
            date = calendar.calendar_query_handler(
                bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
            ).strftime('%Y-%m-%d')
            user_dict.update({str(call.from_user.id): {'date': date}})
            bot.send_message(call.from_user.id, str(user_dict[str(call.from_user.id)]))
            today_month = datetime.today().strftime('%m')
            today_day = datetime.today().strftime('%d')
            if int(month) == int(today_month) and int(day) < int(today_day):
                bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_FAILED_DATE_{lang}'],
                                 reply_markup=show_calendar)
                return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_TIME_{lang}'], reply_markup=base(lang))
            dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_TIME.value)
        elif action == "CANCEL":
            bot.send_message(call.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(call.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(call.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_TIME.value)
def reserve_time(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        today_time = datetime.today().time()
        if message.text[:2].isdigit() and message.text[3:].isdigit() and message.text[2] == ':':
            if int(message.text[:2]) <= 21 and int(message.text[3:]) == 00:
                date_time = datetime.strptime(f'{user_dict[str(message.from_user.id)]["date"]} {message.text}',
                                              '%Y-%m-%d %H:%M')
                datetime_start = f'{date_time}'
                datetime_end = f'{date_time + timedelta(hours=2)}'
                user_dict[str(message.from_user.id)].update({'date_time': date_time})
                user_dict[str(message.from_user.id)].update({'datetime_start': datetime_start})
                user_dict[str(message.from_user.id)].update({'datetime_end': datetime_end})
                bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_CATEGORY_{lang}'],
                                 reply_markup=inline_category(lang))
                dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
            else:
                bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_FAILED_TIME_{lang}'])
        elif message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_DATE_{lang}'],
                             reply_markup=show_calendar)
            dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_DATE.value)
        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_FAILED_TIME_{lang}'])
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')

@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    lang = DataBase.get_user_lang(call.from_user.id)[0]
    if not lang:
        bot.send_message(call.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(call.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        seating_category = 0
        if call.data == trans['booking'][f'TABLES_{lang}']:
            seating_category = 1
            bot.send_photo(call.from_user.id, open('./static/booking/tables.jpeg', 'rb'),
                           trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                           reply_markup=choice_table(user_dict[str(call.from_user.id)]['date_time'], lang))
        elif call.data == trans['booking'][f'CABINS_{lang}']:
            seating_category = 2
            bot.send_photo(call.from_user.id, open('./static/booking/cabins.jpg', 'rb'),
                           trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                           reply_markup=choice_cabins(user_dict[str(call.from_user.id)]['date_time'], lang))
        elif call.data == 'cancel':
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_TIME_{lang}'],
                             reply_markup=base(lang))
            return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_TIME.value)
        user_dict[str(call.from_user.id)].update({'seating_category': seating_category})

        dbworker.set_states(call.from_user.id, config.States.S_CHOICE_SEATING_ID.value)
    except Exception as err:
        bot.send_message(call.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_CHOICE_SEATING_ID.value)
def inline_choice_table(call: types.CallbackQuery):
    lang = DataBase.get_user_lang(call.from_user.id)[0]
    if not lang:
        bot.send_message(call.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(call.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if call.data == 'cancel':
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_CATEGORY_{lang}'],
                             reply_markup=inline_category(lang))
            return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
        table = call.data
        table_id = bookingDB.table_id(table, user_dict[str(call.from_user.id)]['seating_category'])[0]
        user_dict[str(call.from_user.id)].update({'table': table})
        user_dict[str(call.from_user.id)].update({'table_id': table_id})
        bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_PEOPLE_{lang}'],
                         reply_markup=quantity_people(lang))
        dbworker.set_states(call.from_user.id, config.States.S_BOOKING_QUANTITY_PEOPLE.value)
    except Exception as err:
        bot.send_message(call.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_BOOKING_QUANTITY_PEOPLE.value)
def request_people(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        people = message.text
        user_dict[str(message.from_user.id)].update({'people': people})
        if message.text == trans['general'][f'BACK_{lang}']:
            if user_dict[str(message.from_user.id)]['seating_category'] == 1:
                return bot.send_photo(message.from_user.id, open('./static/booking/tables.jpeg', 'rb'),
                               trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                               reply_markup=choice_table(user_dict[str(message.from_user.id)]['date_time'], lang))
            return bot.send_photo(message.from_user.id, open('./static/booking/cabins.jpg', 'rb'),
                           trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                           reply_markup=choice_cabins(user_dict[str(message.from_user.id)]['date_time'], lang))
        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        if people.isdigit() and int(people) != 0:
            if user_dict[str(message.from_user.id)]['seating_category'] == 2:
                min_capacity = user_dict[str(message.from_user.id)]['table_id'][1]
                max_capacity = user_dict[str(message.from_user.id)]['table_id'][2]
                if not min_capacity <= int(people) <= max_capacity:
                    bot.send_message(message.from_user.id,
                                     trans['booking'][f'BOOKING_FAILED_PEOPLE_QUANTITY_{lang}'].
                                     format(min_capacity, max_capacity))
                    bot.send_message(message.from_user.id,
                                     trans['booking'][f'BOOKING_REQUEST_CATEGORY_{lang}'],
                                     reply_markup=inline_category(lang))
                    return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
            bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'],
                             reply_markup=general_nav.send_contact(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)
        bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_FAILED_REQUEST_PEOPLE_{lang}'],
                         reply_markup=quantity_people(lang))

    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    content_types=['contact'])
def request_contact(message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_PEOPLE_{lang}'],
                             reply_markup=quantity_people(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_QUANTITY_PEOPLE.value)

        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)

        phone_number = '+' + message.contact.phone_number
        if ' ' in phone_number:
            phone_number = phone_number.replace(' ', '')
        user_dict[str(message.from_user.id)].update({'phone_number': phone_number})
        bot.send_message(message.from_user.id, trans['general'][f'GET_FIRST_NAME_{lang}'],
                         reply_markup=types.ReplyKeyboardRemove())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def phone(message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_PEOPLE_{lang}'],
                             reply_markup=quantity_people(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_QUANTITY_PEOPLE.value)

        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)

        phone_number = message.text
        if ' ' in phone_number:
            phone_number = phone_number.replace(' ', '')
        user_dict[str(message.from_user.id)].update({'phone_number': phone_number})
        bot.send_message(message.from_user.id, trans['general'][f'GET_FIRST_NAME_{lang}'],
                         reply_markup=types.ReplyKeyboardRemove())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_FIRSTNAME.value)
def get_first_name(message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'],
                             reply_markup=general_nav.send_contact(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)

        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'],
                             reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)

        first_name = message.text
        user_dict[str(message.from_user.id)].update({'first_name': first_name})
        bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_DETAIL_{lang}']
                         .format(first_name, user_dict[str(message.from_user.id)]['phone_number'],
                                 user_dict[str(message.from_user.id)]['datetime_start'].replace("-", "."),
                                 bookingDB.seating_category(user_dict[str(message.from_user.id)]['seating_category'])[0],
                                 user_dict[str(message.from_user.id)]['table'], user_dict[str(message.from_user.id)]['people']),
                         reply_markup=booking_confirm(lang))
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_CONFIRMATION.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_CONFIRMATION.value)
def inline_confirmation(call: types.CallbackQuery):
    lang = DataBase.get_user_lang(call.from_user.id)[0]
    if not lang:
        bot.send_message(call.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(call.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if call.data == 'confirm':
            user = call.from_user.id
            confirm_admin(call, user, user_dict[str(call.from_user.id)]['first_name'],
                          user_dict[str(call.from_user.id)]['phone_number'],
                          user_dict[str(call.from_user.id)]['datetime_start'],
                          user_dict[str(call.from_user.id)]['seating_category'],
                          user_dict[str(call.from_user.id)]['table'],
                          user_dict[str(call.from_user.id)]['people'], lang)
        else:
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_CANCELED_{lang}'],
                             reply_markup=general_nav.back_to_main_page(lang))
            end(call.message)
    except Exception as err:
        bot.send_message(call.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


def confirm_admin(call, user, first_name, phone_number, datetime_start, seating_category, table, people, lang):
    bot.send_message(user, 'Ожидайте подтверждение бронирование от оператора, это займет немного времени')
    bot.send_message(275755142, trans['booking'][f'BOOKING_DETAIL_{lang}']
                     .format(first_name, phone_number, datetime_start.replace("-", "."),
                             bookingDB.seating_category(seating_category)[0], table, people),
                     reply_markup=confirm_keybord(lang))
    return bot.register_next_step_handler(call.message, confirmation_admin, user)


def confirmation_admin(message, user):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'ACCEPT_{lang}']:
            bookingDB.start_booking(message.from_user.id,
                                    user_dict[str(message.from_user.id)]['table_id'][0],
                                    user_dict[str(message.from_user.id)]['datetime_start'],
                                    user_dict[str(message.from_user.id)]['datetime_end'],
                                    user_dict[str(message.from_user.id)]['phone_number'],
                                    user_dict[str(message.from_user.id)]['first_name'],
                                    user_dict[str(message.from_user.id)]['people'])
            bot.send_message(user, trans['booking'][f'BOOKING_CONFIRMED_{lang}'],
                             reply_markup=general_nav.back_to_main_page(lang))
            return dbworker.set_states(user, config.States.S_ACTION_CHOICE.value)
        elif message.text == trans['general'][f'CANCEL_{lang}']:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_ADMIN_CANCEL_{lang}'],
                             reply_markup=general_nav.back_to_main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


############################################################################################


# Доставка
############################################################################################
def delivery(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if not DataBase.get_user(message.from_user.id):
            DataBase.register(message.from_user.id, lang)
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_CATEGORY_{lang}'],
                         reply_markup=food_categoriesRu(lang))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_DELIVERY_MENU_CATEGORY.value)
def dishes(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['delivery'][f'BASKET_{lang}']:
            show_basket(message, lang)
        elif message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            category = message.text
            user_dict.update({str(message.from_user.id): {'category': category}})
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_DISH_{lang}'],
                             reply_markup=dishesRu(deliveryDB.get_categoryId(category, lang)[0], lang=lang))
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_DISHES.value)
def quantity_dish(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['delivery'][f'BASKET_{lang}']:
            show_basket(message, lang)
        elif message.text == trans['general'][f'BACK_{lang}']:
            delivery(message)
        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            dish = message.text
            detail = deliveryDB.get_dish(dish, lang)
            user_dict[str(message.from_user.id)].update({'dish': dish})
            user_dict[str(message.from_user.id)].update({'detail': detail})
            if detail[-1]:
                bot.send_photo(message.from_user.id, open(f'{detail[-1]}', 'rb'),
                               '<b>{0}</b>\n\n'
                               '{1:,} сум'.format(detail[1], detail[2]).replace(",", " "), parse_mode='html',
                               reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_QUANTITY_{lang}'],
                                 reply_markup=numbers(lang))
                dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_QUANTITY.value)
            else:
                bot.send_message(message.from_user.id, '<b>{0}</b>\n\n'
                                                       '{1:,} сум'.format(detail[1], detail[2]).replace(",", " "),
                               parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_QUANTITY_{lang}'],
                                 reply_markup=numbers(lang))
                dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_QUANTITY.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_QUANTITY.value)
def basket(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['delivery'][f'BASKET_{lang}']:
            return show_basket(message, lang)
        elif message.text == trans['general'][f'BACK_{lang}']:
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_DISH_{lang}'],
                             reply_markup=dishesRu(deliveryDB.get_categoryId(
                                 user_dict[str(message.from_user.id)]['category'], lang)[0], lang))
            return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        if message.text.isdigit() and int(message.text) > 0:
            quantity = int(message.text)
            user_dict[str(message.from_user.id)].update({'quantity': quantity})
            bot.send_message(message.from_user.id, user_dict)
            total_price = int(user_dict[str(message.from_user.id)]['detail'][2]) * quantity
            deliveryDB.insert_toBasket(user_dict[str(message.from_user.id)]['detail'][0], quantity, total_price,
                                       message.from_user.id)
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_BASKET_{lang}'],
                             reply_markup=dishesRu(
                                 deliveryDB.get_categoryId(user_dict[str(message.from_user.id)]['category'],
                                                           lang)[0], lang))

            return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_INCORRECT_QUANTITY_{lang}'])

    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')



@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CART.value)
def action_in_basket(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        goods = [good[0] for good in deliveryDB.foods_name(message.from_user.id, lang)]
        del_good = message.text[10:]
        if del_good in goods:
            deliveryDB.delete_good_from_basket(del_good, message.from_user.id, lang)
            show_basket(message, lang)
        elif message.text == trans['delivery'][f'ORDER_{lang}']:
            bot.send_message(message.from_user.id, '<b>Введите адрес доставки</b>',
                             parse_mode='html', reply_markup=send_location(lang))
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CHECKOUT.value)
        elif message.text == trans['general'][f'BACK_TO_MENU_{lang}']:
            delivery(message)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CHECKOUT.value,
    content_types=['location', 'text'])
def takeaway_location_handler(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        address = None
        takeaway = None
        if message.text == trans['delivery'][f'TAKEAWAY_{lang}']:
            takeaway = message.text
        elif message.content_type == 'location':
            latitude = message.location.latitude
            longitude = message.location.longitude
            address = get_address_from_coords(f'{longitude},{latitude}')
        elif message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            address = message.text

        user_dict[str(message.from_user.id)].update({'address': address})
        user_dict[str(message.from_user.id)].update({'takeaway': takeaway})

        bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'],
                         reply_markup=general_nav.send_contact(lang))
        return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    content_types=['contact'])
def request_contact(message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        phone_number = '+' + message.contact.phone_number
        if ' ' in phone_number:
            phone_number = phone_number.replace(' ', '')
        user_dict[str(message.from_user.id)].update({'phone_number': phone_number})
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_PAYMENT_METHOD_{lang}'],
                         parse_mode='html', reply_markup=payment_method(lang))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PAYMENT_METHOD.value)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def request_phone(message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'BACK_TO_MAIN_PAGE_{lang}']:
            bot.send_message(message.from_user.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))#
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        phone_number = message.text
        if ' ' in phone_number:
            phone_number = phone_number.replace(' ', '')
        user_dict[str(message.from_user.id)].update({'phone_number': phone_number})
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_PAYMENT_METHOD_{lang}'],
                         parse_mode='html', reply_markup=payment_method(lang))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PAYMENT_METHOD.value)

    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_DELIVERY_PAYMENT_METHOD.value)
def inline_payment_method(call: types.CallbackQuery):
    lang = DataBase.get_user_lang(call.from_user.id)[0]
    if not lang:
        bot.send_message(call.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(call.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        method_pay = ''
        if call.data == 'cash':
            method_pay = trans['delivery'][f'DELIVERY_CASH_METHOD_{lang}']
        elif call.data == 'payme':
            method_pay = trans['delivery'][f'DELIVERY_PAYME_METHOD_{lang}']
        user_dict[str(call.from_user.id)].update({'method_pay': method_pay})
        bot.send_message(call.from_user.id, user_dict[str(call.from_user.id)])
        accept_client(call.from_user.id,
                      user_dict[str(call.from_user.id)]['phone_number'],
                      method_pay, user_dict[str(call.from_user.id)]['address'],
                      user_dict[str(call.from_user.id)]['takeaway'], lang)
    except Exception as err:
        bot.send_message(call.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CLIENT_ACCEPT.value)
def accepting_client(message: types.Message):
    lang = DataBase.get_user_lang(message.from_user.id)[0]
    if not lang:
        bot.send_message(message.from_user.id, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(message.from_user.id, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'ACCEPT_{lang}']:
            accept_admin(message, message.from_user.id,
                         user_dict[str(message.from_user.id)]['phone_number'],
                         user_dict[str(message.from_user.id)]['method_pay'],
                         user_dict[str(message.from_user.id)]['address'],
                         user_dict[str(message.from_user.id)]['takeaway'], lang)
        elif message.text == trans['general'][f'CANCEL_{lang}']:
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_CANCELED_{lang}'],
                             reply_markup=types.ReplyKeyboardMarkup(True, True).add(types.KeyboardButton('/start')))
            deliveryDB.cancel_order(message.from_user.id)
    except Exception as err:
        bot.send_message(message.from_user.id, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


def accept_admin(message, client, phone_number, method_pay, address, takeaway, lang):
    goods = deliveryDB.get_order(client, lang)
    order_admin = trans['delivery']['DELIVERY_ORDER_ACCEPT_ADMIN_{}'.format(lang)]\
        .format(deliveryDB.order_id(client), address, phone_number, method_pay)
    detail_product = trans['delivery']['DELIVERY_CART_PRODUCT_{}'.format(lang)]
    sum_total = trans['delivery']['DELIVERY_ORDER_ADMIN_TOTAL_{}'.format(lang)]
    if takeaway:
        order_admin = trans['delivery']['DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_{}'.format(lang)]\
            .format(deliveryDB.order_id(client), phone_number, method_pay)
    total = 0
    for good in goods:
        total += int(good[-1])
        order_admin += detail_product.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_admin += sum_total.format(total).replace(',', ' ')
    bot.send_message(client, trans['delivery']['DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_{}'.format(lang)].format(deliveryDB.order_id(client)),
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(275755142, order_admin, parse_mode='html')
    if takeaway:
        bot.send_message(275755142, trans['delivery']['DELIVERY_QUESTION_ACCEPT_{}'.format(lang)],
                         parse_mode='html', reply_markup=accepting_order(lang))
        return bot.register_next_step_handler(message, accepting_admin, client)
    bot.send_message(275755142, trans['delivery']['DELIVERY_COST_{}'.format(lang)], parse_mode='html')
    return bot.register_next_step_handler(message, delivery_amount, client)


def delivery_amount(message: types.Message, client):
    lang = DataBase.get_user_lang(client)[0]
    if not lang:
        bot.send_message(client, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(client, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if not user_dict[str(message.from_user.id)]['takeaway']:
            amount = int(message.text)
            user_dict[str(message.from_user.id)].update({'amount': amount})
            bot.send_message(client, trans['delivery'][f'DELIVERY_QUESTION_ACCEPT_{lang}'], parse_mode='html',
                             reply_markup=accepting_order(lang))
        bot.register_next_step_handler(message, accepting_admin, client)
    except Exception as err:
        bot.send_message(client, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


def accepting_admin(message: types.Message, client):
    lang = DataBase.get_user_lang(client)[0]
    if not lang:
        bot.send_message(client, trans['general']['CHOICE_LANGUAGE'],
                         reply_markup=general_nav.choice_lang())
        return dbworker.set_states(client, config.States.S_CHOICE_LANGUAGE.value)
    try:
        if message.text == trans['general'][f'ACCEPT_{lang}']:
            if user_dict[str(message.from_user.id)]['takeaway']:
                show_order(client, user_dict[str(message.from_user.id)]['phone_number'],
                           user_dict[str(message.from_user.id)]['method_pay'],
                           user_dict[str(message.from_user.id)]['address'],
                           user_dict[str(message.from_user.id)]['takeaway'], lang, amount=0)
            else:
                show_order(client, user_dict[str(message.from_user.id)]['phone_number'],
                           user_dict[str(message.from_user.id)]['method_pay'],
                           user_dict[str(message.from_user.id)]['address'],
                           user_dict[str(message.from_user.id)]['takeaway'], lang,
                           user_dict[str(message.from_user.id)]['amount'])
        elif message.text == trans['general'][f'CANCEL_{lang}']:
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_CANCELED_{lang}'],
                             reply_markup=types.ReplyKeyboardMarkup(True, True).add(types.KeyboardButton('/start')))
            deliveryDB.cancel_order(message.from_user.id)
    except Exception as err:
        bot.send_message(client, trans['general'][f'ERROR_{lang}'], reply_markup=general_nav.error())
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


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
