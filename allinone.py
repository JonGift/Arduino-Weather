import urllib.request
import re

site = urllib.request.urlopen('http://forecast.weather.gov/MapClick.php?CityName=Post+Falls&state=ID&site=OTX&lat=47.7892&lon=-117.027#.U013SVcvm1c')
raw_site_data = str(site.read())
site.close()

forecast_line = re.findall( r'myforecast-current-lrg">..&deg;F', raw_site_data)[0]

temp_str = re.search(r'(\d+)', forecast_line).group(0)
temp = int(temp_str)

if temp > 85:
    heat = 'red'
elif temp < 85 and temp > 50:
    heat = 'green'
elif temp < 50:
    heat = 'blue'

print (heat)