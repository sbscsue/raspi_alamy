import datetime as dt
import time


alarm = dt.time(4,45,0,0)
print(alarm)


while True:
	real=dt.datetime.now().time()
	real = dt.time(real.hour,real.minute,real.second,0)
	print(real)
	if(real==alarm):
		print("wow")
	time.sleep(1)
