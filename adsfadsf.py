from datetime import datetime, timedelta, timezone

offset = timedelta(hours=5)
tz = timezone(offset, name='Tashkent')

today = datetime.now().strftime('%H:%M')


print(today)