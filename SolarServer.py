#import debugpy
#debugpy.listen(5678)
#debugpy.wait_for_client()

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
import Release

logger = mylogging.Logging()
logger.setLogLevel("DEBUG", "False")

logger.Info("Starting SolarServer")
BatVoltage = float()
SolVoltage = float()
chargeCur = float()
mode = int()
supply = SupplyStatus.SupplyStatus(logger)
charger = Victron.Victron(supply, logger, "/dev/ttyUSB0")
Freigabe = Release.Release(charger, logger, "Releases.xml")

#chnge state for the first action
lastStateSolarSupply = not supply.SolarSupply()

while True:
	
	if not supply.IsRunning():
		logger.Error("SupplyStatus Thread was terminated")
	if not charger.IsRunning():
		logger.Error("Victron Thread was terminated")
	if not Freigabe.IsRunning():
		logger.Error("Release Thread was terminated")
		
	time.sleep(60)

	
	
