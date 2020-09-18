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
import Victron
import mylogging

def Freigabe (on):
	global BatVoltage

	if on:
		cmd = "On"
		if (BatVoltage > 26):
			logger.Debug("Bat Voltage: " + str(BatVoltage) + "switch devices on")
		else:
			logger.Debug("Bat Voltage: " + str(BatVoltage) + "leave devices off")
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
			logger.Debug("Freigabe" + str(number) + " switched On")
		elif (jresponse['POWER'] == "OFF"):
			logger.Debug("Freigabe" + str(number) + " switched Off")
		else:
			logger.Error("Error - Freigabe" + str(number) + " returned " + json.dumps(jresponse))

def InformLMAIR (solarSupply):
	control = "off"
	if solarSupply:
		control = "on"
	try:
		response = requests.get("http://lmair/control?cmd=" + control + ",typ%2Cget%2Csmk%2C26%2C1%2Curi%2Clmair%2Fon&id=50")
	except Exception:
		ReadVictron()
		logger.Error("No connection to LMAIR")
		return
	if (response.text != "OK"):
		ReadVictron()
		logger.Error("No response from LMAIR")
		return

logger = mylogging.Logging()
logger.setLogLevel(mylogging.Logging.LOGGLEVEL_DEBUG, True)

logger.Info("Starting SolarServer")

BatVoltage = float()
SolVoltage = float()
chargeCur = float()
mode = int()
supply = SupplyStatus.SupplyStatus()
charger = Victron.Victron(supply, logger, "/dev/tty1")

#chnge state for the first action
lastStateSolarSupply = not supply.SolarSupply()


while True:

	#hast to be switched on
	if supply.SolarSupply() and not lastStateSolarSupply:
		logger.Debug("Solar Power ON")
		Freigabe(True)
		InInformLMAIR(True)

	#hast to be switched off
	if not supply.SolarSupply and lastStateSolarSupply:
		logger.Debug("Solar Power OFF")
		Freigabe(False)
		
		ReadVictron()

	
	
