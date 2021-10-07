import requests

class Temperature(object):
    
    def getOutdoorTemp():
    
       try:
            response = requests.get('http://lmair/weather.json').json()

            return float(response['channel6']['temperature'])
        
       except:
            return -80