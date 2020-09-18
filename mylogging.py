class Logging:
	LOGGLEVEL_NONE=0
	LOGGLEVEL_ERROR=1
	LOGGLEVEL_INFO=2
	LOGGLEVEL_DEBUG=3
	def __init__(self):
		self.__loglevel = 0
		self.__logToCVS = False
		
	def Debug (self, string):
		if self.LOGGLEVEL_DEBUG > self.__loglevel:
			return
		self.__Log("DEBUG - " + string)

	def Info (self, string):
		if self.LOGGLEVEL_INFO > self.__loglevel:
			return
		self.__Log("INFO  - " + string)
	
	def Error (self, string):
		if self.LOGGLEVEL_ERROR > self.__loglevel:
			return
		self.__Log("ERROR - " + string)

	def ToCVS (self, batVoltage, SolarVoltage, mode, current, solarsupply):
		if not self.__logToCVS:
			return
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
		self.__loglevel = loglevel
		
		self.__logToCVS = cvs