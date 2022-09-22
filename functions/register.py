import telebot

from telebot import types
from db import operations


def register(msg, bt):
    text = 'Отлично, вы успешно зарегистрированы'
    if msg.text[:5] == '+998':
        if msg.text[1:].isdigit() and len(msg.text) == 13:
            phone_number = msg.text
            operations.create_user(msg.from_user.id, phone_number)
            return bt.send_message(msg.from_user.id, text)
        return bt.send_message(msg.from_user.id, 'Введите правильный номер телефона')
