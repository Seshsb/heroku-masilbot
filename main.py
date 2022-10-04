from datetime import datetime

import dbworker
import config

from telebot_calendar import *
from connections import *
from flask import request
from keyboards.booking.default import register, navigation
from keyboards.delivery.default.navigations import *
from data.config import *
from keyboards.booking.inline.navigations import *


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
def booking(message):
    bot.send_message(message.from_user.id, BOOKING_REQUEST_DATE,
                     reply_markup=show_calendar)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_DATE.value)


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
            bot.send_message(call.from_user.id, BOOKING_FAILED_DATE, reply_markup=show_calendar)
            return dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_DATE.value)
        bot.send_message(call.from_user.id, BOOKING_REQUEST_TIME)
        dbworker.set_states(call.from_user.id, config.States.S_BOOKING_START_TIME.value)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.send_message(call.from_user.id, f"{calendar_1}: Отменен")


@bot.message_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_START_TIME.value)
def reserve_time(message: types.Message):
    if message.text[:2].isdigit() and message.text[3:].isdigit() and message.text[2] == ':':
        if int(message.text[:2]) <= 21 and int(message.text[3:]) == 00:
            global date_time
            global datetime_start
            global datetime_end
            date_time = datetime.datetime.strptime(f'{date} {message.text}', '%Y-%m-%d %H:%M')
            datetime_start = f'{date_time}'
            datetime_end = f'{date_time + datetime.timedelta(hours=2)}'
            bot.send_message(message.from_user.id, BOOKING_REQUEST_CATEGORY, reply_markup=inline_category())
            dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)
        else:
            bot.send_message(message.from_user.id, BOOKING_FAILED_TIME)
    else:
        bot.send_message(message.from_user.id, BOOKING_FAILED_TIME)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    global seating_category
    if call.data == 'Столы':
        seating_category = 1
        bot.send_photo(call.from_user.id, open('./static/booking/tables.jpeg', 'rb'), BOOKING_GET_TABLEID,
                       reply_markup=choice_table(date_time))
    elif call.data == 'Кабинки':
        seating_category = 2
        bot.send_photo(call.from_user.id, open('./static/booking/cabins.jpg', 'rb'), BOOKING_GET_TABLEID,
                       reply_markup=choice_cabins(date_time))
    dbworker.set_states(call.from_user.id, config.States.S_CHOICE_SEATING_ID.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_CHOICE_SEATING_ID.value)
def inline_choice_table(call: types.CallbackQuery):
    global table_id
    global table
    table = call.data
    table_id = booking.table_id(table, seating_category)
    bot.send_message(call.from_user.id, BOOKING_REQUEST_PEOPLE)
    dbworker.set_states(call.from_user.id, config.States.S_BOOKING_HOW_MANY_PEOPLE.value)


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
    regexp=r'\+998[0-9]{9}$')
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
                                           f'Телефон: {phone_number}\n'
                                           f'Дата и время: {datetime_start.replace("-", ".")}\n'
                                           f'Посадочное место: {booking.seating_category(seating_category)[0]}\n'
                                           f'Стол: {table}\n'
                                           f'Количество человек: {people}', reply_markup=booking_confirm())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_CONFIRMATION.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_CONFIRMATION.value)
def inline_confirmation(call: types.CallbackQuery):
    try:
        if call.data == 'confirm':
            booking.start_booking(call.from_user.id, table_id, datetime_start, datetime_end,phone_number,
                                     first_name, people)
            bot.send_message(call.from_user.id, BOOKING_CONFIRMED, reply_markup=navigation.back_to_menu())
            dbworker.set_states(call.from_user.id, config.States.S_START.value)
        else:
            bot.send_message(call.from_user.id, BOOKING_CANCELED, reply_markup=navigation.back_to_menu())
            dbworker.set_states(call.from_user.id, config.States.S_START.value)
    except:
        bot.send_message(call.from_user.id, '')



############################################################################################


# Доставка
############################################################################################
@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value,
    regexp='Доставка')
def delivery(message):
    if message.text == 'Корзина':
        goods = deliveryDB.show_basket(message.from_user.id)
        cart = f'Корзина\n\n'
        total = 0
        for good in goods:
            total += int(good[2])
            cart += f'{good[1]}x - {good[0]} - {good[2]} сум\n'
        cart = f'\nИтого: {total} сум'
        return bot.send_message(message.from_user.id, cart)
    bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
                     reply_markup=food_categoriesRu())
    dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_MENU_CATEGORY.value)
def dishes(message: types.Message):
    try:
        # if message.text == 'Корзина':
        #     goods = deliveryDB.show_basket(message.from_user.id)
        #     cart = f'Корзина\n\n'
        #     total = 0
        #     for good in goods:
        #         total += int(good[2])
        #         cart += f'{good[1]}x - {good[0]} - {good[2]} сум\n'
        #     cart = f'\nИтого: {total} сум'
        #     return bot.send_message(message.from_user.id, cart)
        global category
        category = message.text
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
                         reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    except:
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
                         reply_markup=food_categoriesRu())


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_DISHES.value)
def quantity_dish(message: types.Message):
    # try:
    # if message.text == 'Корзина':
    #     goods = deliveryDB.show_basket(message.from_user.id)
    #     cart = f'Корзина\n\n'
    #     total = 0
    #     for good in goods:
    #         total += int(good[2])
    #         cart += f'{good[1]}x - {good[0]} - {good[2]} сум\n'
    #     cart = f'\nИтого: {total} сум'
    #     return bot.send_message(message.from_user.id, cart)
    global dish
    global detail
    dish = message.text
    detail = deliveryDB.get_dish(dish)
    bot.send_message(message.from_user.id, f'{detail[1]}\n\n'
                                           f'{detail[2]} сум')
    bot.send_message(message.from_user.id, DELIVERY_REQUEST_QUANTITY,
                     reply_markup=numbers())
    dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_QUANTITY.value)
    # except:
    #     bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
    #                      reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_QUANTITY.value)
def basket(message: types.Message):
    # try:
    global quantity
    quantity = int(message.text)
    total_price = int(detail[2]) * quantity
    deliveryDB.insert_toBasket(detail[0], quantity, total_price, message.from_user.id)
    bot.send_message(message.from_user.id, DELIVERY_BASKET)

    dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    except:
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
                         reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)

#
@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) in config.basket_state, regexp='Корзина')
def show_basket(message: types.Message):
    goods = deliveryDB.show_basket(message.from_user.id)
    cart = f'Корзина\n\n'
    total = 0
    for good in goods:
        total += int(good[2])
        cart += f'{good[1]}x - {good[0]} - {good[2]} сум\n'
    cart = f'\nИтого: {total} сум'
    bot.send_message(message.from_user.id, cart)


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
