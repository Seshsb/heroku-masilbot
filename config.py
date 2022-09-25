from enum import Enum

vdb_file = 'database.vdb'

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ACTION_CHOICE = "choice"
    S_BOOKING = "booking"
    S_BOOKING_SEATING_CATEGORY = "seating category"
    S_BOOKING_START_AT = "start at"
    S_BOOKING_PHONE_NUMBER = "phone number"
    S_CHOICE_TABLE = "choice table"


