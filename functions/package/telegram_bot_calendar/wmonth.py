from .base import DAY
from functions.package.telegram_bot_calendar.detailed import DetailedTelegramCalendar


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY
