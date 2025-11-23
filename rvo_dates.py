from datetime import datetime, date, timedelta
from time import sleep

datetime.today()
datetime.now() #geeft ook het uur mee tot op de milliseconde

def long():
	sleep(5) #wacht 5 seconden, async io bestaat ook -> geeft pc vrij als je wil multithreaden, is iets voor volgend jaar

start_ts = datetime.now() #ts van timestamp
long()
end_ts = datetime.now()

print("This operation took:", end_ts - start_ts, "seconds")

first_of_month = date(2025,11,1)
last_of_month = date(2025,12,1)-timedelta(days=1)
print(first_of_month)
print(last_of_month)

def is_prime(n):
	assert type(n) is int, "must be int"
	assert n>0, "n must be positive"

	if n<=2:
		return True #niet persé waar want één is in principe geen priemgetal

	if n%2 == 0:
		return False
	for i in range (3, n**0,5+1,2):
		if n % i == 0:
			return False
	return True
