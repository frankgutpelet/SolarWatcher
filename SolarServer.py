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
import ThreadWatchdog
import FuelGauge

logger = mylogging.Logging()
logger.setLogLevel("DEBUG", "False")

logger.Info("Starting SolarServer")
BatVoltage = float()
SolVoltage = float()
chargeCur = float()
mode = int()
wd = ThreadWatchdog.ThreadWatchdog(logger)

#fuelGauge = FuelGauge.FuelGauge("Battery.xml", logger)
supply = SupplyStatus.SupplyStatus(logger, wd)
charger = Victron.Victron(supply, logger, "/dev/ttyUSB0", wd)
Freigabe = Release.Release(charger, logger, "Releases.xml", wd)

#chnge state for the first action
lastStateSolarSupply = not supply.SolarSupply()

#endless loop - does not return
wd.watchThreads()


	
	
