import os, time

class FrontEnd(object):

	__instance = None

	def GetInstance(logger):
		if (FrontEnd.__instance == None):
			return FrontEnd(logger)
		return FrontEnd.__instance

	def __init__(self, logger):	
		if FrontEnd.__instance != None:
			raise Exception("This class is a singleton")
		else:
			FrontEnd.__instance = self

		self.batV = 0
		self.batI = 0
		self.SolV = 0
		self.temp = 0
		self.supply = "unknown"
		self.chargingstate = "unknown"
		self.mode = "unknown"
		self.devicelist = dict()
		self.frostschutz = dict()
		self.ontime = dict()
		self.path = "/tmp/solarWatcher.fifo"
		self.logger = logger
		try:
			os.mkfifo(self.path)
		except FileExistsError:
			self.logger.Debug("/tmp/solarWatcher.fifo still exists")
		pass

	def updateDevice(self, name, value, frostschutz, mode, ontime):
		if "AUTO" == mode:
			value = value + "(AUTO)"
		self.devicelist[name] = value
		self.frostschutz[name] = frostschutz
		self.ontime[name] = str(ontime)
		self.logger.Error(name + ": " + self.ontime[name])

	def updateBattery(self, name, number, bat1v, bat2v, current, warning):
		batteryData =  "Battery; " + str(number) + ";" + name + ";" + str(bat1v) + ";" + str(bat2v) +";" + str(current) + ";" + warning
		try:
			self.fifo = open(self.path, "w")
			self.fifo.write(batteryData)

			self.fifo.close()
		except Exception as e:
			self.logger.Error(str(e.with_traceback))


	def updateTemp(self, temp):
		self.temp = temp
	def updateVictronData(self, batV, batI, solV, mode, supply):
		self.batV = batV
		self.batI = batI
		self.solV = solV
		self.mode = mode
		self.supply = supply

	def sendData(self):

		senddata = str(self.batV) + ";" + str(self.batI) + ";" + str(self.solV) + ";" + self.supply + ";" + self.mode + ";" + str(self.temp)
		for device in self.devicelist:
			senddata += ";" + device + " [" + self.ontime[device] + "min];" + self.devicelist[device] + ";" + self.frostschutz[device]
		senddata += "\n"

		try:
			self.fifo = open(self.path, "w")
			self.fifo.write(senddata)
			self.fifo.close()
		except Exception as e:
			self.logger.Error(str(e.with_traceback))





