from .base import MONTH
from functions.package.telegram_bot_calendar.detailed import DetailedTelegramCalendar


class WYearTelegramCalendar(DetailedTelegramCalendar):
    first_step = MONTH
