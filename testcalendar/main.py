import datetime
import telebot
from telebot import types

bot = telebot.TeleBot('5423550151:AAEOLOSI7yPwQcv01btdGUY2YSqlY1I8RAw')
from telebot import TeleBot

from functions.package.telegram_bot_calendar.base import LSTEP
from functions.package.telegram_bot_calendar.detailed import DetailedTelegramCalendar, CalendarWithoutYears



@bot.message_handler(commands=['start'])
def start(m):
    calendar, step = CalendarWithoutYears(min_date=datetime.date.today(),
                                              additional_buttons=[{'text': 'cancel', 'callback_data': 'cancel'}]).build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=lambda c: True)
@bot.callback_query_handler(func=DetailedTelegramCalendar().func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(min_date=datetime.date.today(),
                                              additional_buttons=[{'text': 'cancel', 'callback_data': 'cancel'}]).process(c.data)
    print(c)
    if c.data == 'cancel':
        bot.send_message(c.from_user.id, 'cancel')
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
        bot.send_message(c.message.chat.id, key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
    # elif:
    #     bot.send_message(c.message.chat.id, 'cancel')

# @bot.callback_query_handler(func=lambda call: call.data.startswith('cancel'))
# def call(call):
#     bot.send_message(call.from_user.id, 'cancel')


bot.polling()
