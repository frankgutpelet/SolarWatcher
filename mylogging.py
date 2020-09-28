import datetime
import threading
import time


class Logging:
	LOGGLEVEL_NONE=0
	LOGGLEVEL_ERROR=1
	LOGGLEVEL_INFO=2
	LOGGLEVEL_DEBUG=3
	def __init__(self):
		self.__loglevel = 0
		self.__logToCVS = False
		self.__lock_logBuffer = threading.Lock()
		self.__lock_cvsBuffer = threading.Lock()
		self.logBuffer = list()
		self.cvsBuffer = list()
		self.loggingThread = threading.Thread(target=self.__ThreadFunc, args = ())
		self.loggingThread.start()

	def __ThreadFunc(self):
		logging = False
		while True:
			if (len(self.logBuffer) > 5) or logging:
				logging = False
				try:
					logfile = open("log/solarstatus_" + datetime.datetime.today().strftime("%Y-%m-%d") + ".log", "a")
					self.__lock_logBuffer.acquire()
					for entry in self.logBuffer:
						logfile.write(entry)
					self.logBuffer.clear()
					self.__lock_logBuffer.release()
					logfile.close
				except Exception as e: # logging should not lead to an exception
					print(e)
			else:
				logging = True
			
			if  len(self.cvsBuffer) < 5:
				try:
					logfile = open("log/valuess_" + datetime.datetime.today().strftime("%Y-%m-%d") + ".cvs", "a")
					self.__lock_cvsBuffer.acquire()
					for entry in self.cvsBuffer:
						logfile.write(entry)
					self.cvsBuffer.clear()
					self.__lock_cvsBuffer.release()
					logfile.close
				except Exception: # logging should not lead to an exception
					self.Error("Cannot write to CVS")
					return
			time.sleep(5)
		
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
		self.__lock_cvsBuffer.acquire()
		self.cvsBuffer.append(datetime.datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(batVoltage)+","+str(SolarVoltage)+","+str(current)+","+str(solarsupply)+","+mode+"\n")
		self.__lock_cvsBuffer.release()

	def __Log (self, string):
		self.__lock_logBuffer.acquire()
		self.logBuffer.append(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + string + "\n")
		self.__lock_logBuffer.release()

	def setLogLevel (self, loglevel, cvs):
		if "DEBUG" == loglevel:
			self.__loglevel = Logging.LOGGLEVEL_DEBUG
		elif "INFO" == loglevel:
			self.__loglevel = Logging.LOGGLEVEL_INFO
		elif "ERROR" == loglevel:
			self.__loglevel = Logging.LOGGLEVEL_ERROR
		elif "NONE" == loglevel:
			self.__loglevel = Logging.LOGGLEVEL_NONE
		else:
			self.__loglevel = Logging.LOGGLEVEL_ERROR
			self.Error("Loglevel wrong: " + loglevel)
			loglevel = "DEBUG"
		if "True" == cvs:
			self.__logToCVS = True
			self.Error("Setting loglevel to " + loglevel + " and log to CVS")
		else:
			self.Error("Setting loglevel to " + loglevel + ". Don't log to CVS")