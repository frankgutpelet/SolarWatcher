class Logging:
	def __init__(self):
		self.__loglevel = 0
		self.__logToCVS = False
		
	def Debug (self, string):
		if 3 > self.__loglevel:
			return
		self.__Log("DEBUG - " + string)

	def Info (self, string):
		if 2 > self.__loglevel:
			return
		self.__Log("INFO  - " + string)
	
	def Error (self, string):
		if 1 > self.__loglevel:
			return
		self.__Log("ERROR - " + string)

	def ToCVS (self, batVoltage, SolarVoltage, mode, current, solarsupply):
		try:
			logfile = open("values.csv", "a")
			logfile.write(datetime.datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(batVoltage)+","+str(SolarVoltage)+","+str(mode)+","+str(current)+","+str(solarsupply)+"\n")
			logfile.close
		except Exception: # logging should not lead to an exception
			self.Error("Cannot write to CVS")
			return

	def __Log (self, string):
		try:
			logfile = open("solarstatus_" + datetime.datetime.today().strftime("%Y-%m-%d") + ".log", "a")
			logfile.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + string + "\n")
			logfile.close
		except Exception: # logging should not lead to an exception
			return
	
	def setLogLevel (self, loglevel, cvs):
		if("Quiet" == loglevel):
			self.__loglevel = 0
		elif ("Error" == loglevel):
			self.__loglevel = 1
		elif ("Info" == loglevel):
			self.__loglevel = 2
		if("Debug" == loglevel):
			self.__loglevel = 3
		else:
			raise ValueError("Wrong Parameter for LogLevel: " + loglevel)
		
		self.__logToCVS = cvs