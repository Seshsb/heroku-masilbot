import traceback
try:
    name = int(input())
except Exception as err:
    print(traceback.format_exc())