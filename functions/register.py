from db import operations
from data.config import REGISTER_VALID, REGISTER_INVALID, FORMAT_NUMBER_INVALID


def register(message, bot):
    if message.text[:4] == '+998':
        if message.text[1:].isdigit() and len(message.text) == 13:
            phone_number = message.text
            operations.create_user(message.from_user.id, phone_number)
            return bot.send_message(message.from_user.id, REGISTER_VALID)
        return bot.send_message(message.from_user.id, REGISTER_INVALID)

    elif message.text[1:].isdigit and message.text[:4] != '+998':
        return bot.send_message(message.from_user.id, REGISTER_INVALID)

    elif message.content_type == 'contact':
        if message.contact.phone_number[:3] == '998' and len(message.contact.phone_number) == 12:
            phone_number = '+' + message.contact.phone_number
        elif message.contact.phone_number[0:4] == '+998' and len(message.contact.phone_number) == 12:
            phone_number = message.contact.phone_number
        else:
            return bot.send_message(message.from_user.id, FORMAT_NUMBER_INVALID)

        operations.create_user(message.from_user.id, phone_number)
        return bot.send_message(message.from_user.id, REGISTER_VALID)


