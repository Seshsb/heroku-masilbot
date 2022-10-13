from datetime import datetime

import dbworker
import config

from telebot_calendar import *
from connections import *
from flask import request
from keyboards import back_to_menu
from keyboards.booking.default import register, navigation
from keyboards.delivery.default.navigations import *
from data.config import *
from keyboards.booking.inline.navigations import *
from functions.handlers import get_address_from_coords


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def back_to_menu(message: types.Message):
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value)
def booking_or_delivery(message):
    if message.text == 'Бронирование':
        bot.send_message(message.from_user.id, BOOKING_REQUEST_DATE,
                         reply_markup=show_calendar)
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_DATE.value)
    elif message.text == 'Доставка':
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
                         reply_markup=food_categoriesRu())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)


# Бронирование
############################################################################################
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
        bot.send_message(call.from_user.id, BOOKING_REQUEST_TIME, reply_markup=types.ReplyKeyboardRemove())
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
    table_id = bookingDB.table_id(table, seating_category)
    bot.send_message(call.from_user.id, BOOKING_REQUEST_PEOPLE, reply_markup=types.ReplyKeyboardRemove())
    dbworker.set_states(call.from_user.id, config.States.S_BOOKING_QUANTITY_PEOPLE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_BOOKING_QUANTITY_PEOPLE.value)
def request_people(message: types.Message):
    global people
    people = message.text
    if people.isdigit():  # Сделать обработку людей
        bot.send_message(message.from_user.id, GET_PHONE_NUMBER, reply_markup=register.send_contact())
        dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    content_types=['contact'])
def request_contact(message):
    global phone_number
    phone_number = '+' + message.contact.phone_number
    bot.send_message(message.from_user.id, GET_FIRST_NAME, reply_markup=types.ReplyKeyboardRemove())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def phone(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, GET_FIRST_NAME, reply_markup=types.ReplyKeyboardRemove())
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
                                           f'Посадочное место: {bookingDB.seating_category(seating_category)[0]}\n'
                                           f'Стол: {table}\n'
                                           f'Количество человек: {people}', reply_markup=booking_confirm())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_CONFIRMATION.value)


@bot.callback_query_handler(
    func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_CONFIRMATION.value)
def inline_confirmation(call: types.CallbackQuery):
    try:
        if call.data == 'confirm':
            bookingDB.start_booking(call.from_user.id, table_id, datetime_start, datetime_end, phone_number,
                                    first_name, people)
            bot.send_message(call.from_user.id, BOOKING_CONFIRMED, reply_markup=back_to_menu())
            dbworker.set_states(call.from_user.id, config.States.S_START.value)
        else:
            bot.send_message(call.from_user.id, BOOKING_CANCELED, reply_markup=back_to_menu())
            dbworker.set_states(call.from_user.id, config.States.S_START.value)
    except:
        bot.send_message(call.from_user.id, '')


############################################################################################


# Доставка
############################################################################################
@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        message.from_user.id) == config.States.S_DELIVERY_MENU_CATEGORY.value)
def dishes(message: types.Message):
    # try:
    if message.text == 'Корзина':
        show_basket(message)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
        return dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    else:
        global category
        category = message.text
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
                         reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    # except:
    #     bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
    #                      reply_markup=food_categoriesRu())


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_DISHES.value)
def quantity_dish(message: types.Message):
    # try:
    if message.text == 'Корзина':
        show_basket(message)
    elif message.text == 'Назад':
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
                         reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))

        return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)
    elif message.text == 'Вернуться на главную страницу':
        bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    else:
        global dish
        global detail
        dish = message.text
        detail = deliveryDB.get_dish(dish)
        bot.send_photo(message.from_user.id, open(f'{detail[-1]}', 'rb'), f'<b>{detail[1]}</b>\n\n'
                                                                          f'{detail[2]} сум', parse_mode='html',
                       reply_markup=types.ReplyKeyboardRemove())
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
    if message.text == 'Корзина':
        show_basket(message)
    elif message.text == 'Назад':
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_QUANTITY,
                         reply_markup=numbers())
        return dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    elif message.text == 'Вернуться на главную страницу':
        bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    else:
        global quantity
        quantity = int(message.text)
        total_price = int(detail[2]) * quantity
        deliveryDB.insert_toBasket(detail[0], quantity, total_price, message.from_user.id)
        bot.send_message(message.from_user.id, DELIVERY_BASKET,
                         reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))

        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)
    # except:
    #     bot.send_message(message.from_user.id, DELIVERY_REQUEST_DISH,
    #                      reply_markup=dishesRu(deliveryDB.get_categoryId(category)[0]))
    #     dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_DISHES.value)


def show_basket(message: types.Message):
    goods = deliveryDB.show_basket(message.from_user.id)
    cart = f'<b>Корзина:</b>\n\n'
    total = 0
    for good in goods:
        total += int(good[-1])
        cart += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    cart += '\n<b>Итого: {0:,} сум</b>'.format(total).replace(',', ' ')
    bot.send_message(message.from_user.id, cart, reply_markup=order(message.from_user.id), parse_mode='html')
    dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CART.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CART.value)
def action_in_basket(message: types.Message):
    goods = [good[0] for good in deliveryDB.foods_name(message.from_user.id)]
    del_good = message.text[10:]
    if del_good in goods:
        deliveryDB.delete_good_from_basket(del_good, message.from_user.id)
        show_basket(message)
    elif message.text == 'Оформить заказ':
        bot.send_message(message.from_user.id, '<b>Введите адрес доставки</b>',
                         parse_mode='html', reply_markup=send_location())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CHECKOUT.value)
    elif message.text == 'Вернуться на главную страницу':
        bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())
        dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_CHECKOUT.value,
    content_types=['location', 'text'])
def takeaway_location_handler(message: types.Message):
    global address
    if message.text == 'На вынос 🏃🏻‍♂️':
        bot.send_message(message.from_user.id, GET_PHONE_NUMBER)
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_TAKEAWAY_PHONENUMBER.value)
    elif message.content_type == 'location':
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = get_address_from_coords(f'{longitude},{latitude}')
        bot.send_message(message.from_user.id, GET_PHONE_NUMBER)
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)
    elif message.content_type == 'text':
        address = message.text
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_PHONENUMBER.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_TAKEAWAY_PHONENUMBER.value,
    content_types=['contact'])
def takeaway_request_contact(message):
    phone_number = '+' + message.contact.phone_number
    deliveryDB.checkout(message.from_user.id, address, phone_number)
    bot.send_message(message.from_user.id, f'Спасибо, ваш заказ <b>{deliveryDB.order_id(message.from_user.id)} '
                                           f'передан на обработку. Ожидайте подтверждения заказа от бота</b>.',
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())



@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_TAKEAWAY_PHONENUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def takeaway_phone(message):
    phone_number = message.text
    deliveryDB.checkout(message.from_user.id, address, phone_number)
    bot.send_message(message.from_user.id, f'Спасибо, ваш заказ #<b>{deliveryDB.order_id(message.from_user.id)}</b> '
                                           f'передан на обработку. Ожидайте подтверждения заказа от бота.',
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    content_types=['contact'])
def request_contact(message):
    phone_number = '+' + message.contact.phone_number
    deliveryDB.checkout(message.from_user.id, address, phone_number)
    bot.send_message(message.from_user.id, f'Спасибо, ваш заказ <b>{deliveryDB.order_id(message.from_user.id)} '
                                           f'передан на обработку. Ожидайте подтверждения заказа от бота</b>.',
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())



@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_DELIVERY_PHONENUMBER.value,
    regexp=r'\+998[0-9]{9}$')
def phone(message):
    global phone_number
    phone_number = message.text
    deliveryDB.checkout(message.from_user.id, address, phone_number)
    bot.send_message(message.from_user.id, f'Спасибо, ваш заказ <b>{deliveryDB.order_id(message.from_user.id)} '
                                           f'передан на обработку. Ожидайте подтверждения заказа от бота</b>.',
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


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
