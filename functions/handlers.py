from pprint import pprint

import requests

import config
import dbworker
from connections import YANDEX_TOKEN, bot

from data.config import *
from keyboards import general_nav
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
    cart = f'<b>Корзина:</b>\n\n\n'
    total = 0
    if goods:
        for good in goods:
            total += int(good[-1])
            cart += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
        cart += '\n<b>Итого: {0:,} сум</b>'.format(total).replace(',', ' ')
        bot.send_message(message.from_user.id, cart, reply_markup=order(message.from_user.id), parse_mode='html')
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_CART.value)
    else:
        bot.send_message(message.from_user.id, '<b>\nКорзина пуста.\n</b>', parse_mode='html')
        bot.send_message(message.from_user.id, DELIVERY_REQUEST_CATEGORY,
                         reply_markup=food_categoriesRu())
        dbworker.set_states(message.from_user.id, config.States.S_DELIVERY_MENU_CATEGORY.value)


def accept_admin(client, phone_number, method_pay, address, takeaway):
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
    order_admin += '\n<b>Сумма заказа: {0:,} сум</b>'.format(total).replace(',', ' ')
    bot.send_message(client,
                     f'Спасибо за ожидание, ваш заказ <b>#{deliveryDB.order_id(client)}</b> '
                     f'передан на обработку. С вами свяжется оператор.',
                     parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(275755142, order_admin, parse_mode='html')
    if takeaway:
        bot.send_message(275755142, '<b>Подтвердить заказ?</b>', parse_mode='html', reply_markup=accepting_order())
        return dbworker.set_states(275755142, config.States.S_DELIVERY_ADMIN_ACCEPT.value)
    bot.send_message(275755142, "<b>Введите сумму доставки</b>", parse_mode='html')
    return dbworker.set_states(275755142, config.States.S_DELIVERY_AMOUNT.value)


def accept_client(client, phone_number, method_pay, address, takeaway):
    goods = deliveryDB.get_order(client)
    order_client = f'<b>Ваш заказ</b>\n' \
                   f'Тип заказа: <b>{takeaway if takeaway else "Доставка 🚘"}</b>\n' \
                   f'Адрес: <b>{takeaway if takeaway else address}</b>\n' \
                   f'Номер телефона: <b>{phone_number}</b>\n' \
                   f'Метод оплаты: <b>{method_pay}</b>\n\n\n'
    if takeaway:
        order_client = f'<b>Ваш заказ</b>\n' \
                       f'Тип заказа: <b>{takeaway}</b>\n' \
                       f'Адрес ресторана: <b>Мирабад, 41</b>\n' \
                       f'Номер телефона: <b>{phone_number}</b>\n' \
                       f'Метод оплаты: <b>{method_pay}</b>\n\n\n'
    total = 0
    for good in goods:
        total += int(good[-1])
        order_client += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_client += '\n<b>Сумма заказа: {0:,} сум + стоимость доставки (определяется исходя отадреса доставки)</b>\n\n' \
                   'Для связи с оператором @seshsb'.format(total,).replace(',', ' ')
    bot.send_message(client, order_client, parse_mode='html', reply_markup=accepting_order())
    deliveryDB.checkout(client, address, phone_number)
    dbworker.set_states(client, config.States.S_DELIVERY_CLIENT_ACCEPT.value)


def show_order(client, phone_number, method_pay, address, takeaway, amount):
    goods = deliveryDB.get_order(client)
    order_client = f'<b>Заказ #{deliveryDB.order_id(client)}</b>\n' \
            f'Тип заказа: <b> "Доставка 🚘"</b>\n' \
            f'Адрес: <b>{takeaway if takeaway else address}</b>\n' \
            f'Номер телефона: <b>{phone_number}</b>\n' \
            f'Метод оплаты: <b>{method_pay}</b>\n' \
            f'Время получения заказа: <b>В ближайшее время</b>\n\n\n'
    if takeaway:
        order_client = f'<b>Ваш заказ</b>\n' \
                       f'Тип заказа: <b>{takeaway}</b>\n' \
                       f'Адрес ресторана: <b>Мирабад, 41</b>\n' \
                       f'Номер телефона: <b>{phone_number}</b>\n' \
                       f'Метод оплаты: <b>{method_pay}</b>\n\n\n'
    total = 0
    for good in goods:
        total += int(good[-1])
        order_client += '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'.format(good[0], good[2], good[1], good[-1]).replace(',', ' ')
    order_client += '\n<b>Сумма заказа: {0:,} сум\n' \
                   'Сумма доставки: {1:,}\n' \
                   'Итого: {2:,}</b>\n\n'.format(total, amount, total+amount).replace(',', ' ')
    bot.send_message(client, order_client, parse_mode='html')
    deliveryDB.accept_order(client)
    bot.send_message(client, 'Хотите что-то еще?', reply_markup=general_nav.booking_or_delivery())
    bot.send_message(client, 'Благодарим за заказ,', reply_markup=general_nav.booking_or_delivery())
    dbworker.set_states(client, config.States.S_ACTION_CHOICE.value)
