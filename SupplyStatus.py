import threading 
import time
import RPi.GPIO as GPIO


class SupplyStatus:

	gpioPin = 4

	def __init__(self, logger, watchdog):
		self.__solarSupply = False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.ReadThread = threading.Thread(target=self.__ReadThread, args = ())
		self.logger = logger
		self.watchdog = watchdog
		self.wdIndex = watchdog.subscribe("SupplyStatus", 3)
		self.ReadThread.start()
		
		


	def IsRunning (self):
		if self.ReadThread.isAlive():
			return True
		else:
			#self.ReadThread.start()
			return False

	def SolarSupply(self):
		return self.__solarSupply

	def __ReadThread(self):
		self.logger.Debug("start SupplyStatus Thread")
		while True:
			self.watchdog.trigger(self.wdIndex)
			try:

				#wait for 2 seconds for falling edge (sample 100ms)
				if  None != GPIO.wait_for_edge(self.gpioPin, GPIO.FALLING, timeout=2000):
					if 1 == GPIO.input(self.gpioPin):	#debounce
						continue
					#self.logger.Debug("Wait for falling edge")
					self.__solarSupply = True
				else:
					#no falling edge - indicator does not blink anymore
					self.__solarSupply = False
			except Exception as e:
				self.logger.Error("SolarSupply: " + str(e))
				GPIO.setmode(GPIO.BCM)
				GPIO.setup(self.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
