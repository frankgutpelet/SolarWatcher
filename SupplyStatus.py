import threading 
import time
import RPi.GPIO as GPIO


class SupplyStatus:
	def __init__(self, logger):
		self.__solarSupply = False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.ReadThread = threading.Thread(target=self.__ReadThread, args = ())
		self.logger = logger
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
			#pegel is low - LED is blinking 
			if (0 == GPIO.input(27)):
				if not self.__solarSupply:	#only set if it is not set
					self.__solarSupply = True
				time.sleep(5)
			else:
				#wait for 2 seconds for falling edge (sample 100ms)
				while  None != GPIO.wait_for_edge(27, GPIO.FALLING, timeout=2000):
					self.logger.Debug("Wait for falling edge")
					pass

				#no falling edge - indicator does not blink anymore
				if self.__solarSupply:	#only reset if it is set
					self.__solarSupply = False
