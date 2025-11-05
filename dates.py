from datetime import datetime, date, timedelta
from time import sleep

def long():
    sleep(5)

first_of_month = date(2025,11, 1)
last_of_month = date(2025,12,31) - timedelta(days=1)

start_ts = datetime.now()

long()

end_ts = datetime.now()

print("This operation took: ", end_ts - start_ts, "seconds.")