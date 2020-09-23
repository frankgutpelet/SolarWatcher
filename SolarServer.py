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
logger.setLogLevel(mylogging.Logging.LOGGLEVEL_DEBUG, True)

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
	
		
	time.sleep(5)

	
	
