from datetime import datetime

message = '23:00'
time_now = datetime.now().time()
if datetime.strptime(message, '%H:%M').time() > time_now:
    print(True)
print(False)