from enum import Enum

vdb_file = 'database.vdb'

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = 'start'# Начало нового диалога
    S_ACTION_CHOICE = "choice"
    S_BOOKING = "booking"
    S_BOOKING_SEATING_CATEGORY = "seating category"
    S_CHOICE_TABLE = "choice table"
    S_CHOICE_CABINS = "choice cabins"
    S_BOOKING_START_DATE = "start date"
    S_BOOKING_START_TIME = "start time"
    S_BOOKING_PHONE_NUMBER = "phone number"
    S_BOOKING_FIRSTNAME = "first name"
    S_CHOICE_TABLE_ID = "choice table id"
    S_CHOICE_TABLE_ID_INLINE = "choice table id inline"


