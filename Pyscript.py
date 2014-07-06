import urllib.request
import re
import serial
import time
import datetime
from datetime import timedelta

ser = serial.Serial("COM3", 9600) #Start serial with Arduino on COM3

def get_temp():
	#Function that downloads data from the internet. I live in Post Falls, so it downloads Post Falls.
	try:
		site = urllib.request.urlopen('http://forecast.weather.gov/MapClick.php?CityName=Post+Falls&state=ID&site=OTX&lat=47.7892&lon=-117.027#.U013SVcvm1c')
	except:
		return 0
	raw_site_data = str(site.read()) #log the data.
	site.close()

	forecast_line = re.findall( r'myforecast-current-lrg">..&deg;F', raw_site_data)[0] #Find the temperature in Fahrenheit.

	temp_str = re.search(r'(\d+)', forecast_line).group(0) #Evil bit level hacking (just kidding)
	temp = int(temp_str) #Creates an int for the temperature.
	if temp:
		return temp
	else:
		return 0 #returns a number like 85.

statictime = datetime.date.today() #Used if you keep the Arduino running.
statictemp = get_temp()


ser.read() #You have to read before you can write.
while True:
	currenthour = datetime.datetime.now().hour #Used with line 21.
	currenttime = datetime.date.today()
	temp = get_temp()
	if currenttime - statictime > timedelta(hours=24) and currenthour > 8: #Used to update the second temperature bit.
		if temp > statictemp:
			ser.write(str('6').encode())
		elif temp <= statictemp:
			ser.write(str('7').encode())
		statictemp = temp
		statictime = currenttime
		
	if temp > 95: #Decide what to send to the Arduino
		heat = '1'
	elif temp <95 and temp > 85:
		heat = '2'
	elif temp < 85 and temp > 65:
		heat = '3'
	elif temp < 65:
		heat = '4'
	
	try:	
		ser.write(str(heat).encode()) #Sends the Arduino an encoded string.
	except:
		try:
			ser = serial.Serial("COM3", 9600)
		except:
			pass
	time.sleep(3600) #Wait for an hour.
		