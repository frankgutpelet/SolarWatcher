import xml.etree.ElementTree as ET
import threading
import time
import os.path
from datetime import datetime
import requests
import FrontendInterface
import Temperature

maxPowerConsumptionWatt = 3000
voltageThresholdP100W = 0.2

class switch:
	SUPPLY_MAINS = 0
	SUPPLY_SOLAR = 1
	SUPPLY_ALL = 2

	def __init__(self, No, ontime, offtime, voltage, name, prio, maxpower, supply, tempMin):
		self.no = No
		self.hourOn = int(ontime.split(":")[0])
		self.minuteOn = int(ontime.split(":")[1])
		self.hourOff = int(offtime.split(":")[0])
		self.minuteOff = int(offtime.split(":")[1])
		self.name = name
		self.voltage = float(voltage)
		self.prio = int(prio)
		self.maxpower = int(maxpower)
		self.isOn = False
		self.switchNumber = 0
		self.supply = supply
		self.tempMin = float(tempMin)
		self.tempProtection = False


class Release:
	def __init__(self, charger, logger, configfile, watchdog):
		self.configfile = configfile
		self.logger = logger
		self.switches = list()
		self.charger = charger
		self.mainPower = 0
		self.devicesOn = {}
		self.parseConfig()
		self.configTimestamp = os.path.getmtime(configfile)
		self.wdIndex = watchdog.subscribe("Release", 10)
		self.watchdog = watchdog
		self.frontendif = FrontendInterface.FrontEnd.GetInstance(logger)
		self.ReleaseThread = threading.Thread(target=self.__ReleaseThread, args = ())
		self.ReleaseThread.start()

	def IsRunning (self):
		if self.ReleaseThread.isAlive():
			return True
		else:
			#self.ReleaseThread.start()
			return False

	def __ReleaseThread (self):
		global voltageThresholdP100W

		self.logger.Debug("Start Release Thread")

		for sw in self.switches:
			self.Switch(sw, False)

		while True:
			self.frontendif.updateTemp(Temperature.Temperature.getOutdoorTemp())
			for sw in self.switches:
				if self.Ontime(sw):	#Zeitschaltuhr
					if(		(switch.SUPPLY_ALL == sw.supply)																					#all supply
						or	((switch.SUPPLY_MAINS == sw.supply) and (False == self.charger.solarSupply.SolarSupply()))										#mains supply
						or	((switch.SUPPLY_SOLAR == sw.supply) and (self.charger.solarSupply.SolarSupply())and(sw.voltage <= self.charger.batVoltage))):		#solar supply
						tresholdVoltage = sw.voltage + (voltageThresholdP100W*sw.maxpower/100)
						if ((switch.SUPPLY_SOLAR == sw.supply) and (tresholdVoltage > self.charger.batVoltage)):		# do nothing when treshold not reached
							self.logger.Debug(sw.name + "will be switched at " + str(tresholdVoltage) )
							continue
						self.logger.Debug("Bat: " + str(self.charger.batVoltage) + "V")
						self.Switch(sw, True)
					else:
						self.Switch(sw, False)
				else:
					self.Switch(sw, False)

				if sw.tempMin >= Temperature.Temperature.getOutdoorTemp():	#Frostschutz
					self.Switch(sw, True)
					sw.tempProtection = True
					self.logger.Debug("protect " + sw.name + " for low temperature (" + str(Temperature.Temperature.getOutdoorTemp()) + "°C)")
				elif sw.tempProtection and (sw.tempMin < (Temperature.Temperature.getOutdoorTemp() + 0.2)):
					self.Switch(sw, False)
					sw.tempProtection = False
					self.logger.Debug("switch off protection for  " + sw.name + " for low temperature (" + str(Temperature.Temperature.getOutdoorTemp()) + "°C)")

			self.HandleRelease()
			if self.configTimestamp != os.path.getmtime(self.configfile):
				self.configTimestamp = os.path.getmtime(self.configfile)
				self.parseConfig()
			time.sleep(5)
			self.watchdog.trigger(self.wdIndex)


	def Ontime(self, sw):
		minutes = datetime.now().hour * 60 + datetime.now().minute
		ontime = sw.hourOn * 60 + sw.minuteOn
		offtime = sw.hourOff * 60 + sw.minuteOff

		#in case of 0:00
		if (offtime == 0):
			offtime = 1440
		if(ontime <= minutes)and(minutes < offtime):
			return True
		return False



	def HandleRelease(self):
		global maxPowerConsumptionWatt
		mainPower = 0
		cmd = "off"

		for prio in range(1, 10):
			for sw in self.switches:
				cmd = "off"
				if self.DeviceIsOn(sw.name):
					cmd = "on"
				if sw.prio != prio: continue
				if sw.isOn:
					if (maxPowerConsumptionWatt > (mainPower + sw.maxpower)):
						cmd = "on"
						mainPower += sw.maxpower
						self.logger.Debug("switch " + sw.name + " on. Power consumption sum = " + str(mainPower) + "W" )
					else:
						self.logger.Debug("switch " + sw.name + " off. Power consumption would be too high: sum = " + str(mainPower + sw.maxpower) + "W") 
				
				try:
					response = requests.get("http://Solarfreigabe" + str(sw.no) + "/cm?cmnd=Power%20" + cmd )
					
				except Exception:	
					self.logger.Error("No connection to Solarfreigabe" + str(sw.no))
					continue

		self.mainPower = mainPower
	
	def DeviceIsOn (self, device):
		for dev in self.devicesOn[device]:
			if dev: return True
		return False

	def Switch (self, sw, on):
		
		if on:
			if not sw.isOn:
				self.logger.Debug("Switch " + sw.name + " on")
				sw.isOn = True
				self.devicesOn[sw.name][sw.switchNumber] = True
				self.frontendif.updateDevice(sw.name, "on", str(sw.tempProtection))
		else:
			if sw.isOn:
				self.logger.Debug("Switch " + sw.name + " off")
				sw.isOn = False
				self.devicesOn[sw.name][sw.switchNumber] = False
				self.frontendif.updateDevice(sw.name, "off", "False")

	def parseConfig(self):
		try:
			config = ET.parse(self.configfile)
		except Exception:
			self.logger.Error("configfile not valid xml")
			return
		root = config.getroot()
		try:
			self.devicesOn.clear()
			self.switches.clear()
			self.logger.setLogLevel(root.find('Logging').attrib['loglevel'], root.find('Logging').attrib['cvs'])
		except Exception:
			self.logger.Error("configfile not well formed - cannot change loglevel")

		for release in root.findall('Release'):
			try:
				no = release.attrib['number']
				name = release.attrib['name']
				prio = release.attrib['prio']
				maxpower = release.attrib['maxpower']
			except Exception:
				self.logger.Error("Configfile is not well formed: Element " + release.tag)
			for cur_switch in release.findall('Switch'):
				if "solar" == cur_switch.attrib['supply']:
					supply = switch.SUPPLY_SOLAR
				elif "all" == cur_switch.attrib['supply']:
					supply = switch.SUPPLY_ALL
				elif "mains" == cur_switch.attrib['supply']:
					supply = switch.SUPPLY_MAINS
				else:
					self.logger.Error("Config not well formed - Element Release(" + name + ")/" + cur_switch.tag + " - supply: wrong wording")

				if "False" == cur_switch.attrib['enable']: continue
				elif "True" != cur_switch.attrib['enable']:
					self.logger.Error("Config not well formed - Element Release(" + name + ")/" + cur_switch.tag + " - enable: wrong wording")
					continue
				if 'frostschutz' in cur_switch.attrib:
					tempMin = cur_switch.attrib['frostschutz']
				else:
					tempMin = -50
				try:
					new_switch = switch(no, cur_switch.attrib['on'], cur_switch.attrib['off'], cur_switch.attrib['voltage'], name, prio, maxpower, supply, tempMin)
				except Exception:
					self.logger.Error("Configfile is not well formed: Element Release(" + name + ")/" + cur_switch.tag)
					continue
				
				if None == self.devicesOn.get(name):
					self.devicesOn[name] = list()
				self.devicesOn[name].append(False)
				new_switch.switchNumber = (len(self.devicesOn[name]) - 1)
				self.switches.append(new_switch)

		self.logger.Debug("Release Configuration updated successful")