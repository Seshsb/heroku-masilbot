import telebot.apihelper

import config
import dbworker
from connections import *

from datetime import datetime
from telebot import types
from keyboards.default import register, navigation
from db import operations
from data.config import GET_PHONE_NUMBER, BOOKING_SUCCESS


def choice_tableid(tbl_id):
    tables = [table[0] for table in operations.tables()]
    return tables[tbl_id-1]