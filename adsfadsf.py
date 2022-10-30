from datetime import datetime, timedelta, timezone, time

import pytz

offset = timedelta(hours=12)
tz = timezone(offset, name='Tashkent')

today = datetime.now().strftime('%H:%M')
today10 = datetime.now(tz=tz).strftime('%H:%M')

if time(11, 00) > datetime.now(tz=tz).replace(tzinfo=pytz.UTC).time() > time(23, 00):
    print('True')


print(today)
print(today10)