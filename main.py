import traceback
import telebot.apihelper
import telebot.storage
from telebot.types import CallbackQuery

import dbworker
import config

from db import DataBase
from datetime import datetime
from connections import *
from flask import request
from keyboards import general_nav
from keyboards.delivery.default.navigations import *
from keyboards.delivery.inline.navigations import *
from data.config import *
from keyboards.booking.inline.navigations import *
from functions.handlers import get_address_from_coords, show_basket, accept_admin, show_order, accept_client


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        if DataBase.get_user(message.from_user.id):
            global lang
            lang = DataBase.get_user_lang(message.from_user.id)
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'],
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
    try:
        global lang
        if message.text == 'Русский 🇷🇺':
            lang = trans['general']['LANGUAGE_RU']
        elif message.text == '(Корейский) 🇰🇷':
            lang = trans['general']['LANGUAGE_KO']

        if DataBase.get_user(message.from_user.id):
            DataBase.change_lang(message.from_user.id, lang)
            bot.send_message(message.from_user.id, trans['general'][f'CHANGE_LANG_SUCCESS_{lang}'])
        else:
            DataBase.register(message.from_user.id, lang)
        bot.send_message(message.chat.id, trans['general'][f'START_{lang}'],
                         reply_markup=general_nav.main_page(lang))
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_END.value)
def end(message: types.Message):
    try:
        bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')

@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value)
def booking_or_delivery(message: types.Message):
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
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


# Бронирование
############################################################################################
def booking(message: types.Message):
    try:
        bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_DATE_{lang}'],
                         reply_markup=show_calendar)
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_DATE.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_DATE.value)
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_date(call: CallbackQuery):
    try:
        global date
        name, action, year, month, day = call.data.split(calendar_1.sep)
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
        ).strftime('%Y-%m-%d')

        if action == "DAY":
            today_month = datetime.date.today().strftime('%m')
            today_day = datetime.date.today().strftime('%d')
            if int(month) == int(today_month) and int(day) < int(today_day):
                bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_FAILED_DATE_{lang}'],
                                 reply_markup=show_calendar)
                return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_TIME_{lang}'], reply_markup=types.ReplyKeyboardRemove())
            dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_TIME.value)
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Cancellation",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            bot.send_message(call.from_user.id, f"{calendar_1}: Отменен")
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_TIME.value)
def reserve_time(message: types.Message):
    try:
        if message.text[:2].isdigit() and message.text[3:].isdigit() and message.text[2] == ':':
            if int(message.text[:2]) <= 21 and int(message.text[3:]) == 00:
                global date_time
                global datetime_start
                global datetime_end
                date_time = datetime.datetime.strptime(f'{date} {message.text}', '%Y-%m-%d %H:%M')
                datetime_start = f'{date_time}'
                datetime_end = f'{date_time + datetime.timedelta(hours=2)}'
                bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_REQUEST_CATEGORY_{lang}'],
                                 reply_markup=inline_category(lang))
                dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
            else:
                bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_FAILED_TIME_{lang}'])
        else:
            bot.send_message(message.from_user.id, trans['booking'][f'BOOKING_FAILED_TIME_{lang}'])
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')

@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    try:
        global seating_category
        if call.data == trans['booking'][f'TABLES_{lang}']:
            seating_category = 1
            bot.send_photo(call.from_user.id, open('./static/booking/tables.jpeg', 'rb'),
                           trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                           reply_markup=choice_table(date_time))
        elif call.data == trans['booking'][f'CABINS_{lang}']:
            seating_category = 2
            bot.send_photo(call.from_user.id, open('./static/booking/cabins.jpg', 'rb'),
                           trans['booking'][f'BOOKING_GET_TABLEID_{lang}'],
                           reply_markup=choice_cabins(date_time, lang))
        dbworker.set_states(call.from_user.id, config.States.S_CHOICE_SEATING_ID.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_CHOICE_SEATING_ID.value)
def inline_choice_table(call: types.CallbackQuery):
    try:
        global table_id
        global table
        table = call.data
        table_id = bookingDB.table_id(table, seating_category)[0]
        bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_REQUEST_PEOPLE_{lang}'], reply_markup=types.ReplyKeyboardRemove())
        dbworker.set_states(call.from_user.id, config.States.S_BOOKING_QUANTITY_PEOPLE.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_BOOKING_QUANTITY_PEOPLE.value)
def request_people(message: types.Message):
    try:
        global people
        people = message.text
        if people.isdigit():
            if seating_category == 2:
                min_capacity = table_id[1]
                max_capacity = table_id[2]
                if not min_capacity <= int(people) <= max_capacity:
                    bot.send_message(message.from_user.id,
                                     trans['booking'][f'BOOKING_FAILED_PEOPLE_{lang}'].format(min_capacity, max_capacity))
                    bot.send_message(message.from_user.id,
                                     trans['booking'][f'BOOKING_REQUEST_CATEGORY_{lang}'],
                                     reply_markup=inline_category(lang))
                    return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
        bot.send_message(message.from_user.id, trans['booking'][f'GET_PHONE_NUMBER_{lang}'],
                         reply_markup=general_nav.send_contact(lang))
        return dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)

    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    content_types=['contact'])
def request_contact(message):
    try:
        global phone_number
        phone_number = '+' + message.contact.phone_number
        bot.send_message(message.from_user.id, trans['booking']['GET_FIRST_NAME_{lang}'],
                         reply_markup=types.ReplyKeyboardRemove())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def phone(message):
    try:
        global phone_number
        phone_number = message.text
        bot.send_message(message.from_user.id, trans['booking']['GET_FIRST_NAME_{lang}'],
                         reply_markup=types.ReplyKeyboardRemove())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_FIRSTNAME.value)
def get_first_name(message):
    try:
        global first_name
        first_name = message.text
        bot.send_message(message.from_user.id, trans['booking']['BOOKING_DETAIL_{lang}']
                         .format(first_name, phone_number, datetime_start.replace("-", "."),
                                 bookingDB.seating_category(seating_category)[0], table, people),
                         reply_markup=booking_confirm(lang))
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_CONFIRMATION.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_CONFIRMATION.value)
def inline_confirmation(call: types.CallbackQuery):
    try:
        if call.data == 'confirm':
            bookingDB.start_booking(call.from_user.id, table_id[0], datetime_start, datetime_end, phone_number,
                                    first_name, people)
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_CONFIRMED_{lang}'],
                             reply_markup=general_nav.back_to_main_page(lang))
            dbworker.set_states(call.from_user.id, config.States.S_START.value)
        else:
            bot.send_message(call.from_user.id, trans['booking'][f'BOOKING_CANCELED_{lang}'],
                             reply_markup=general_nav.back_to_main_page(lang))
            dbworker.set_states(call.from_user.id, config.States.S_END.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


############################################################################################


# Доставка
############################################################################################
def delivery(message: types.Message):
    try:
        global client
        client = message.from_user.id
        bot.send_message(message.from_user.id, trans['delivery']['DELIVERY_REQUEST_CATEGORY_{lang}'],
                         reply_markup=food_categoriesRu())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_DELIVERY_MENU_CATEGORY.value)
def dishes(message: types.Message):
    try:
        if message.text == 'Корзина':
            show_basket(message, lang)
        elif message.text == 'Назад':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            global category
            category = message.text
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_DISH_{lang}'],
                             reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_DISHES.value)
def quantity_dish(message: types.Message):
    try:
        if message.text == 'Корзина':
            show_basket(message, lang)
        elif message.text == 'Назад':
            delivery(message)
        elif message.text == 'Вернуться на главную страницу':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            global dish
            global detail
            dish = message.text
            detail = deliveryDB.get_dish(dish)
            if detail[-1]:
                bot.send_photo(message.from_user.id, open(f'{detail[-1]}', 'rb'),
                               '<b>{0}</b>\n\n'
                               '{1:,} сум'.format(detail[1], detail[2]).replace(",", " "), parse_mode='html',
                               reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_QUANTITY_{lang}'],
                                 reply_markup=numbers())
                dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_QUANTITY.value)
            else:
                bot.send_message(message.from_user.id, '<b>{0}</b>\n\n'
                                                       '{1:,} сум'.format(detail[1], detail[2]).replace(",", " "),
                               parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_QUANTITY_{lang}'],
                                 reply_markup=numbers())
                dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_QUANTITY.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_QUANTITY.value)
def basket(message: types.Message):
    try:
        if message.text == 'Корзина':
            return show_basket(message, lang)
        elif message.text == 'Назад':
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_REQUEST_DISH_{lang}'],
                             reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
            return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
        elif message.text == 'Вернуться на главную страницу':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        if message.text.isdigit() and int(message.text) > 0:
            global quantity
            quantity = int(message.text)
            total_price = int(detail[2]) * quantity
            deliveryDB.insert_toBasket(detail[0], quantity, total_price, message.from_user.id)
            bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_BASKET_{lang}'],
                             reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))

            return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_INCORRECT_QUANTITY_{lang}'])

    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')



@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CART.value)
def action_in_basket(message: types.Message):
    try:
        goods = [good[0] for good in deliveryDB.foods_name(message.from_user.id)]
        del_good = message.text[10:]
        if del_good in goods:
            deliveryDB.delete_good_from_basket(del_good, message.from_user.id)
            show_basket(message, lang)
        elif message.text == 'Оформить заказ':
            bot.send_message(message.from_user.id, '<b>Введите адрес доставки</b>',
                             parse_mode='html', reply_markup=send_location())
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CHECKOUT.value)
        elif message.text == 'Вернуться в меню доставки':
            delivery(message)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CHECKOUT.value,
    content_types=['location', 'text'])
def takeaway_location_handler(message: types.Message):
    try:
        global address
        global takeaway
        takeaway = None
        address = None
        if message.text == 'На вынос 🏃🏻‍♂️':
            takeaway = message.text
            bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'],
                             reply_markup=general_nav.send_contact())
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)
        elif message.content_type == 'location':
            latitude = message.location.latitude
            longitude = message.location.longitude
            address = get_address_from_coords(f'{longitude},{latitude}')
            bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'], reply_markup=general_nav.send_contact())
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)
        elif message.text == 'Вернуться на главную страницу':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        else:
            address = message.text
            bot.send_message(message.from_user.id, trans['general'][f'GET_PHONE_NUMBER_{lang}'], reply_markup=general_nav.send_contact())
            dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    content_types=['contact'])
def request_contact(message):
    try:
        if message.text == 'Вернуться на главную страницу':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        global phone_number
        phone_number = '+' + message.contact.phone_number
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_PAYMENT_METHOD_{lang}'],
                         parse_mode='html', reply_markup=payment_method())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PAYMENT_METHOD.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def request_phone(message):
    try:
        if message.text == 'Вернуться на главную страницу':
            bot.send_message(message.chat.id, trans['general'][f'START_{lang}'], reply_markup=general_nav.main_page(lang))#
            return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
        global phone_number
        phone_number = message.text
        bot.send_message(message.from_user.id, trans['delivery'][f'DELIVERY_PAYMENT_METHOD_{lang}'],#
                         parse_mode='html', reply_markup=payment_method())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PAYMENT_METHOD.value)

    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_DELIVERY_PAYMENT_METHOD.value)
def inline_payment_method(call: types.CallbackQuery):
    try:
        global method_pay
        if call.data == 'cash':
            method_pay = trans['delivery'][f'DELIVERY_CASH_METHOD_{lang}']
        elif call.data == 'payme':
            method_pay = trans['delivery'][f'DELIVERY_PAYME_METHOD_{lang}']
        accept_client(client, phone_number, method_pay, address, takeaway, lang)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_DELIVERY_CLIENT_ACCEPT.value)
def accepting_client(call: types.CallbackQuery):
    try:
        if call.data == 'accept':
            accept_admin(client, phone_number, method_pay, address, takeaway,lang)
        elif call.data == 'cancel':
            bot.send_message(client, trans['delivery'][f'DELIVERY_CANCELED_{lang}'],
                             reply_markup=types.ReplyKeyboardMarkup(True, True).add(types.KeyboardButton('/start')))
            deliveryDB.cancel_order(client)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
                                    f'{traceback.format_exc()}')

@bot.message_handler(
    func=lambda message: dbworker.get_current_state(275755142) == config.States.S_DELIVERY_AMOUNT.value)
def delivery_amount(message: types.Message):
    try:
        global amount
        if not takeaway:
            amount = int(message.text)
            bot.send_message(275755142, trans['delivery'][f'DELIVERY_QUESTION_ACCEPT_{lang}'], parse_mode='html', reply_markup=accepting_order())
        dbworker.set_states(275755142, config.States.S_DELIVERY_ADMIN_ACCEPT.value)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {message.from_user.id}:\n'
                                    f'{traceback.format_exc()}')


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(275755142) == config.States.S_DELIVERY_ADMIN_ACCEPT.value)
def accepting_admin(call: types.CallbackQuery):
    try:
        if call.data == 'accept':
            if takeaway:
                show_order(client, phone_number, method_pay, address, takeaway, lang, amount=0)
            else:
                show_order(client, phone_number, method_pay, address, takeaway, lang, amount)
        elif call.data == 'cancel':
            bot.send_message(client, trans['delivery'][f'DELIVERY_CANCELED_{lang}'],
                             reply_markup=types.ReplyKeyboardMarkup(True, True).add(types.KeyboardButton('/start')))
            deliveryDB.cancel_order(client)
    except Exception as err:
        bot.send_message(275755142, f'Ошибка юзера {call.from_user.id}:\n'
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
