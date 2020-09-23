import Release
import time

class log:
	def __init__(self):
		pass
	def Debug(self, text):
		print("Debug:" + text + "\n")

	def Error(self, text):
		print("Error:" + text + "\n")

class solarsup:
	def __init__(self):
		self.ss = True
		pass
	def SolarSupply(self):
		return self.ss

class charge:
	def __init__(self):
		self.batVoltage = 27.5
		self.solVoltage = 60
		self.solarSupply = solarsup()

logger = log()
charger = charge()
Release.Release(charger, logger, "Releases.xml")

while True:
	time.sleep(10)
