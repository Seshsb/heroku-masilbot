from pprint import pprint

import requests
from telebot import types

import config
import dbworker
from connections import YANDEX_TOKEN, bot

#создаем функцию get_address_from_coords с параметром coords, куда мы будем посылать координаты и получать готовый адрес.
from data.config import *
from db import deliveryDB
from keyboards.delivery.default.navigations import *
from keyboards.delivery.inline.navigations import accepting_order


def get_address_from_coords(coords):
    #заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
    PARAMS = {
        "apikey": YANDEX_TOKEN,
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    #отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        pprint(r)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        #возвращаем полученный адрес
        return address_str
    except Exception as e:
        #если не смогли, то возвращаем ошибку
        return "error"


def show_basket(message: types.Message):

    '''Вывод корзины'''

    goods = deliveryDB.show_basket(message.from_user.id)
    cart = f'<b>Корзина:</b>\n\n'
    total = 0
    if goods:
        for good in goods:
            total += int(good[-1])
            cart += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
        cart += '\n<b>Итого: {0:,} сум</b>'.format(total).replace(',', ' ')
        bot.send_message(message.from_user.id, cart, reply_markup=order(message.from_user.id), parse_mode='html')
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CART.value)
    else:
        bot.send_message(message.from_user.id, '<b>Корзина пуста</b>', parse_mode='html')
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
                         reply_markup=food_categoriesRu())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)


def show_order_admin(client, phone_number, method_pay, address, takeaway):
    goods = deliveryDB.get_order(client)
    order_admin = f'<b>Заказ #{deliveryDB.order_id(client)}</b>\n' \
            f'Тип заказа: {takeaway if takeaway else "Доставка 🚘"}\n' \
            f'Адрес: {takeaway if takeaway else address}\n' \
            f'Номер телефона: {phone_number}\n' \
            f'Метод оплаты: {method_pay}\n\n\n'
    total = 0
    for good in goods:
        total += int(good[-1])
        order_admin += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_admin += '\n\n<b>Сумма заказа: {0:,} сум</b>'.format(total).replace(',', ' ')
    bot.send_message(275755142, order_admin, parse_mode='html')
    bot.send_message(275755142, "<b>Введите сумму доставки</b>", parse_mode='html')
    dbworker.set_states(275755142, config.States.S_DELIVERY_AMOUNT.value)


def show_order_client(client, phone_number, method_pay, address, takeaway, amount):
    goods = deliveryDB.get_order(client)
    order_admin = f'<b>Заказ #{deliveryDB.order_id(client)}</b>\n' \
            f'Тип заказа: <b>{takeaway if takeaway else "Доставка 🚘"}</b>\n' \
            f'Адрес: <b>{takeaway if takeaway else address}</b>\n' \
            f'Номер телефона: <b>{phone_number}</b>\n' \
            f'Метод оплаты: <b>{method_pay}</b>\n' \
            f'Время получения заказа: <b>В ближайшее время</b>\n\n\n'
    total = 0
    for good in goods:
        total += int(good[-1])
        order_admin += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_admin += '\n\n<b>Сумма заказа: {0:,} сум\n' \
                   'Сумма доставки: {1:,}\n' \
                   'Итого: {2:,}</b>\n\n' \
                   'Для связи с оператором @seshsb'.format(total, amount, total+amount).replace(',', ' ')
    bot.send_message(client, order_admin, parse_mode='html', reply_markup=accepting_order())
    dbworker.set_states(client, config.States.S_DELIVERY_CLIENT_ACCEPTING.value)

