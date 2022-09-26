import dbworker
import config

from connections import *
from telebot import types
from flask import request
from functions.handlers import reserve_time, get_table_id
from keyboards.default import navigation
from data.config import START, GET_TABLEID, GET_FIRST_NAME
from keyboards.inline.navigations import inline_category


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)
    bot.send_message(message.chat.id, START, reply_markup=navigation.booking_or_delivery())


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ACTION_CHOICE.value, regexp='Бронирование')
def text(message):
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING.value)
    bot.send_message(message.from_user.id, 'Выберите категорию посадочных мест',
                    reply_markup=inline_category())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_SEATING_CATEGORY.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_START_AT.value, content_types=['contact'])
def request_contact(message):
    phone_number = '+' + message.contact.phone_number
    bot.send_message(message.from_user.id, GET_FIRST_NAME)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_START_AT.value, regexp=r'\+998[0-9]{9,9}$')
def phone(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, GET_FIRST_NAME)
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_PHONE_NUMBER.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_BOOKING_PHONE_NUMBER.value)
def get_first_name(message):
    first_name = message.text
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_FIRSTNAME.value)
    bot.send_message(message.from_user.id, GET_TABLEID)
    bot.register_next_step_handler(message, get_table_id, phone_number, first_name)


@bot.callback_query_handler(func=lambda call: dbworker.get_current_state(call.from_user.id) == config.States.S_BOOKING_SEATING_CATEGORY.value)
def inline_seating_category(call: types.CallbackQuery):
    if call.data == 'tables':
        dbworker.set_states(call.from_user.id, config.States.S_CHOICE_TABLE.value)
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
