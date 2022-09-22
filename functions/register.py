import telebot

from telebot import types
from db import operations


def register(message, bot):
    text = 'Отлично, вы успешно зарегистрированы'
    if message.text[:4] == '+998':
        if message.text[1:].isdigit() and len(message.text) == 13:
            phone_number = message.text
            operations.create_user(message.from_user.id, phone_number)
            return bot.send_message(message.from_user.id, text)
        return bot.send_message(message.from_user.id, 'Введите правильный номер телефона')
