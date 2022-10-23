from pprint import pprint

import requests

import config
import dbworker
from connections import YANDEX_TOKEN, bot

from data.config import *
from db import *
from keyboards import general_nav
from keyboards.delivery.default.navigations import *
from keyboards.delivery.inline.navigations import accepting_order


########################################################################################################
# Бронирование
# def request_phone_number(message):


########################################################################################################
# Доставка
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


def show_basket(message: types.Message, lang):

    '''Вывод корзины'''

    goods = deliveryDB.show_basket(message.from_user.id, lang)
    cart = trans['delivery']['DELIVERY_CART_{}'.format(lang)]
    detail_product = trans['delivery']['DELIVERY_CART_PRODUCT_{}'.format(lang)]
    sum_total = trans['delivery']['DELIVERY_CART_TOTAL_{}'.format(lang)]
    total = 0
    if goods:
        for good in goods:
            total += int(good[-1])
            cart += detail_product.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
        cart += sum_total.format(total).replace(',', ' ')
        bot.send_message(message.from_user.id, cart, reply_markup=order(message.from_user.id, lang), parse_mode='html')
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CART.value)
    else:
        bot.send_message(message.from_user.id, trans['delivery']['DELIVERY_CART_EMPTY_{}'.format(lang)], parse_mode='html')
        bot.send_message(message.from_user.id, trans['delivery']['DELIVERY_REQUEST_CATEGORY_{}'.format(lang)],
                         reply_markup=food_categoriesRu(lang))
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)


def accept_admin(client, phone_number, method_pay, address, takeaway, lang):
    goods = deliveryDB.get_order(client, lang)
    order_admin = trans['delivery']['DELIVERY_ORDER_ACCEPT_ADMIN_{}'.format(lang)]\
        .format(deliveryDB.order_id(client), address, phone_number, method_pay)
    detail_product = trans['delivery']['DELIVERY_CART_PRODUCT_{}'.format(lang)]
    sum_total = trans['delivery']['DELIVERY_ORDER_ADMIN_TOTAL_{}'.format(lang)]
    if takeaway:
        order_admin = trans['delivery']['DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_{}'.format(lang)]\
            .format(deliveryDB.order_id(client), phone_number, method_pay)
    total = 0
    for good in goods:
        total += int(good[-1])
        order_admin += detail_product.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_admin += sum_total.format(total).replace(',', ' ')
    bot.send_message(client, trans['delivery']['DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_{}'.format(lang)].format(deliveryDB.order_id(client)),
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(275755142, order_admin, parse_mode='html')
    if takeaway:
        bot.send_message(275755142, trans['delivery']['DELIVERY_QUESTION_ACCEPT_{}'.format(lang)],
                         parse_mode='html', reply_markup=accepting_order(lang))
        return dbworker.set_states(275755142, config.States.S_DELIVERY_ADMIN_ACCEPT.value)
    bot.send_message(275755142, trans['delivery']['DELIVERY_COST_{}'.format(lang)], parse_mode='html')
    return dbworker.set_states(275755142, config.States.S_DELIVERY_AMOUNT.value)


def accept_client(client, phone_number, method_pay, address, takeaway, lang):
    goods = deliveryDB.get_order(client, lang)
    order_client = trans['delivery']['DELIVERY_ORDER_ACCEPT_CLIENT_{}'.format(lang)]\
        .format(address, phone_number, method_pay)
    detail_product = trans['delivery']['DELIVERY_CART_PRODUCT_{}'.format(lang)]
    if takeaway:
        order_client = trans['delivery']['DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_{}'.format(lang)]\
            .format(phone_number, method_pay)
    total = 0
    for good in goods:
        total += int(good[-1])
        order_client += detail_product.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_client += trans['delivery']['DELIVERY_ORDER_CLIENT_TOTAL_{}'.format(lang)].format(total,).replace(',', ' ')
    bot.send_message(client, order_client, parse_mode='html', reply_markup=accepting_order(lang))
    deliveryDB.checkout(client, address, phone_number)
    dbworker.set_states(client, config.States.S_DELIVERY_CLIENT_ACCEPT.value)


def show_order(client, phone_number, method_pay, address, takeaway, lang, amount):
    goods = deliveryDB.get_order(client, lang)
    order_client = trans['delivery']['DELIVERY_ORDER_{}'.format(lang)]\
        .format(deliveryDB.order_id(client), address, phone_number, method_pay)
    detail_product = trans['delivery']['DELIVERY_CART_PRODUCT_{}'.format(lang)]
    if takeaway:
        order_client = trans['delivery']['DELIVERY_ORDER_TAKEAWAY_{}'.format(lang)]\
            .format(deliveryDB.order_id(client), phone_number, method_pay)
    total = 0
    for good in goods:
        total += int(good[-1])
        order_client += detail_product.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_client += trans['delivery']['DELIVERY_ORDER_SUM_TOTAL_{}'.format(lang)].format(total, amount, total+amount).replace(',', ' ')
    bot.send_message(client, order_client, parse_mode='html')
    deliveryDB.accept_order(client)
    bot.send_message(client, trans['delivery']['DELIVERY_SOMETHING_ELSE_{}'.format(lang)], reply_markup=general_nav.main_page(lang))
    bot.send_message(client, trans['delivery']['DELIVERY_THANKS_{}'.format(lang)], reply_markup=general_nav.main_page(lang))
    dbworker.set_states(client, config.States.S_ACTION_CHOICE.value)
