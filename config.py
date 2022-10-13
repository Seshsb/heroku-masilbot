from enum import Enum

vdb_file = 'database.vdb'

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = 'start'  # Начало нового диалога
    S_ACTION_CHOICE = "choice"

    # Бронирование
    S_BOOKING_SEATING_CATEGORY = "seating category"
    S_CHOICE_SEATING_ID = "choice seating id"
    S_BOOKING_START_DATE = "start date"
    S_BOOKING_START_TIME = "start time"
    S_BOOKING_QUANTITY_PEOPLE = "quantity people"
    S_BOOKING_PHONE_NUMBER = "phone number"
    S_BOOKING_FIRSTNAME = "first name"
    S_BOOKING_CONFIRMATION = "booking confirmation"

    # Доставка
    S_DELIVERY_MENU_CATEGORY = 'menu category'
    S_DELIVERY_DISHES = 'dishes'
    S_DELIVERY_QUANTITY = 'quantity'
    S_DELIVERY_CART = 'cart'
    S_DELIVERY_CHECKOUT = 'checkout'
    S_DELIVERY_TAKEAWAY_PHONENUMBER = 'takeaway phonenumber'
    S_DELIVERY_PHONENUMBER = 'delivery phonenumber'
    S_DELIVERY_PAYMENT_METHOD = 'payment method'
    S_DELIVERY_AMOUNT = 'delivery amount'
    S_DELIVERY_ADMIN_ACCEPTING = 'admin accepting'
    S_DELIVERY_CLIENT_ACCEPTING = 'client accepting'
