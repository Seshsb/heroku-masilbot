from datetime import datetime
from telebot import types
from keyboards.default import register
from db import operations
from data.config import GET_PHONE_NUMBER, GET_TABLEID


def reserve_time(message: types.Message, bot):
    time = message.text
    global time_sql
    time_sql = f'{str(datetime.today().year)}-{time[3:5]}-{time[:2]} {time[6:]}'
    bot.send_message(message.from_user.id, GET_PHONE_NUMBER, reply_markup=register.send_contact())
    # bot.register_next_step_handler(message, get_phone_number, time)


def get_phone_number(message: types.Message, time, bot):
    phone_number = message.contact.phone_number
    bot.send_message(message.from_user.id, GET_TABLEID)
    bot.register_next_step_handler(message, get_table_id, time, phone_number)


def get_table_id(message: types.Message, phone_number):
    table_id = message.text
    operations.start_booking(table_id, time_sql, phone_number)
    bot.send_message(message.from_user.id, table_id)

#
# @bot.message_handler(func=get_phone_number, content_types=['text', 'contact'])
# def test(message):
#     bot.send_message(message.from_user.id, 'test')