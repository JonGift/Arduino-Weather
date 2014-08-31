#Currently broken because some idiots updated the layout of the site.
import urllib.request
import re
import serial
import time
import datetime
from datetime import timedelta
import json

ser = serial.Serial("COM3", 9600) #Start serial with Arduino on COM3

def get_temp():
	#Function that downloads data from the internet. I live in Post Falls, so it downloads Post Falls.
	try:
		f = urllib.request.urlopen('http://api.wunderground.com/api/0e026670d6a5e764/geolookup/conditions/q/ID/Post_Falls.json')
	except:
		return 0
	json_string = f.read().decode("UTF-8")
	parsed_json = json.loads(json_string)
	temp_f = parsed_json['current_observation']['temp_f']
	f.close()
	
	temp = round(int(temp_f)) #Creates an int for the temperature.
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
	if currenttime - statictime > timedelta(hours=1) and currenthour > 8: #Used to update the second temperature bit.
		if temp > statictemp: #Need a try except here
			try:
				ser.write(str('6').encode())
			except:
				pass
		elif temp <= statictemp:
			try:
				ser.write(str('7').encode())
			except:
				pass
		statictemp = temp
		statictime = currenttime
		
	if temp >= 95: #Decide what to send to the Arduino
		heat = '1'
	elif temp < 95 and temp >= 70:
		heat = '2'
	elif temp < 70 and temp >= 30:
		heat = '3'
	elif temp < 30:
		heat = '4'
	
	try:	
		ser.write(str(heat).encode()) #Sends the Arduino an encoded string.
	except:
		try:
			ser = serial.Serial("COM3", 9600)
		except:
			pass
	time.sleep(3600) #Wait for an hour.
		