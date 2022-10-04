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
    S_BOOKING_HOW_MANY_PEOPLE = "how many people"
    S_BOOKING_PHONE_NUMBER = "phone number"
    S_BOOKING_FIRSTNAME = "first name"
    S_BOOKING_CONFIRMATION = "booking confirmation"

    # Доставка
    S_DELIVERY_MENU_CATEGORY = 'menu category'
    S_DELIVERY_DISHES = 'dishes'
    S_DELIVERY_QUANTITY = 'quantity'


basket_state = [
    States.S_DELIVERY_MENU_CATEGORY.value,
    States.S_DELIVERY_DISHES.value,
    States.S_DELIVERY_QUANTITY.value,
]
print(basket_state)