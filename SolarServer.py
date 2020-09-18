import RPi.GPIO as GPIO
import time
import datetime
import requests
import json
import serial
import io
import sys
import re
import SupplyStatus


def log (string):
	logfile = open("solarstatus_" + datetime.datetime.today().strftime("%Y-%m-%d") + ".log", "a")
	logfile.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + string + "\n")
	logfile.close

def csv (batVoltage, SolarVoltage, mode, current, solarsupply):
	logfile = open("values.csv", "a")
	logfile.write(datetime.datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(batVoltage)+","+str(SolarVoltage)+","+str(mode)+","+str(current)+","+str(solarsupply)+"\n")
	logfile.close

def Freigabe (on):
	global BatVoltage

	if on:
		cmd = "On"
		if (BatVoltage > 26):
			log ("Bat Voltage: " + str(BatVoltage) + "switch devices on")
		else:
			log ("Bat Voltage: " + str(BatVoltage) + "leave devices off")
			return
	else:
		cmd = "Off"

	for number in range(1, 10):
		try:
			response = requests.get("http://Solarfreigabe" + str(number) + "/cm?cmnd=Power%20" + cmd, )
		except Exception:		
			continue
		if None == response:
			continue;
		jresponse = response.json()
		if (jresponse['POWER'] ==  "ON"):
			log("Freigabe" + str(number) + " switched On")
		elif (jresponse['POWER'] == "OFF"):
			log("Freigabe" + str(number) + " switched Off")
		else:
			log("Error - Freigabe" + str(number) + " returned " + json.dumps(jresponse))

def ReadVictron ():
	global lastStateSolarSupply
	ser = serial.Serial('/dev/ttyUSB0', 19200)
	
	global BatVoltage
	global SolVoltage
	global chargeCur
	global mode

	ser.flush()
	for i in range(1, 20):
		line = str(ser.readline())
		try:
			pair = line.split('\\r\\n')[0].split('b\'')[1].split('\\t')
		except IndexError:
			log("Error cannot parse text: " + line)
			return
		
		if ('V' == pair[0]):
			BatVoltage = int(pair[1])/1000
		elif ('VPV' == pair[0]):
			SolVoltage = int(pair[1])/1000
		elif ('I' == pair[0]):
			chargeCur = int(pair[1])/1000
		elif ('MPPT' == pair[0]):
			mode = int(pair[1])/1000

	csv(BatVoltage, SolVoltage, mode, chargeCur, lastStateSolarSupply)

def InformLMAIR (solarSupply):
	control = "off"
	if solarSupply:
		control = "on"
	try:
		response = requests.get("http://lmair/control?cmd=" + control + ",typ%2Cget%2Csmk%2C26%2C1%2Curi%2Clmair%2Fon&id=50")
	except Exception:
		ReadVictron()
		log("No connection to LMAIR")
		return
	if (response.text != "OK"):
		ReadVictron()
		log("No response from LMAIR")
		return


log("starting service")

BatVoltage = float()
SolVoltage = float()
chargeCur = float()
mode = int()
supply = SupplyStatus.SupplyStatus()

#chnge state for the first action
lastStateSolarSupply = not supply.SolarSupply()


while True:

	#hast to be switched on
	if supply.SolarSupply() and not lastStateSolarSupply:
		log("Solar Power ON")
		Freigabe(True)
		InInformLMAIR(True)

	#hast to be switched off
	if not supply.SolarSupply and lastStateSolarSupply:
		log("Solar Power OFF")
		Freigabe(False)
		
		ReadVictron()

	
	
