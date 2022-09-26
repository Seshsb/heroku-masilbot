import config
import dbworker
from connections import *

from datetime import datetime
from telebot import types
from keyboards.default import register
from db import operations
from data.config import GET_PHONE_NUMBER, BOOKING_SUCCESS


def reserve_time(message: types.Message):
    time = message.text
    global time_sql
    time_sql = f'{str(datetime.today().year)}-{time[3:5]}-{time[:2]} {time[6:]}'
    bot.send_message(message.from_user.id, GET_PHONE_NUMBER, reply_markup=register.send_contact())
    dbworker.set_states(message.from_user.id, config.States.S_BOOKING_START_AT.value)


def get_table_id(message: types.Message, phone_number, first_name):
    table_id = message.text
    operations.start_booking(message.from_user.id, table_id, time_sql, phone_number)
    dbworker.set_states(message.from_user.id, config.States.S_CHOICE_TABLE_ID.value)
    bot.send_message(message.from_user.id, BOOKING_SUCCESS)
    dbworker.set_states(message.from_user.id, config.States.S_ACTION_CHOICE.value)

#
# @bot.message_handler(func=get_phone_number, content_types=['text', 'contact'])
# def test(message):
#     bot.send_message(message.from_user.id, 'test')