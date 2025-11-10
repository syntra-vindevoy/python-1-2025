from datetime import datetime, date, timedelta
from time import sleep

def long():
    sleep(5)


first_of_month = date(2025, 11, 1)
last_of_month = date(2025, 12, 1) - timedelta(days=1)
