import telebot

from telebot import types
from db import operations


def register(msg, bt):
    phone_number = msg.contact.phone_number
    text = 'Отлично, вы успешно зарегистрированы'
    if msg.text[:5] == '+998':
        phone_number = msg.text
        if phone_number[1:].isdigit() and len(phone_number) == 13:
            operations.create_user(msg.from_user.id, phone_number)
            return bt.send_message(msg.from_user.id, text)
        return bt.send_message(msg.from_user.id, 'Введите правильный номер телефона')
