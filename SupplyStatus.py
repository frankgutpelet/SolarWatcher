import threading 
import time
import RPi.GPIO as GPIO


class SupplyStatus:
	def __init__(self):
		self.__solarSupply = False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.ReadThread = threading.Thread(target=self.__ReadThread, args = ())

	def SolarSupply(self):
		ret = self.__solarSupply

	def setSolarSupply(solarSupply):
		self.__solarSupply = solarSupply

	def __ReadThread(self):

		while True:
			#pegel is low - LED is blinking 
			if (0 == GPIO.input(17)):
				if not self.__solarSupply:	#only set if it is not set
					self.__solarSupply = True
			else:
				#wait for 2 seconds for falling edge (sample 100ms)
				for sample in range(1, 20):
					if (0 == GPIO.input(17)):
						continue
					time.sleep(0.1)

				#no falling edge - indicator does not blink anymore
				if self.__solarSupply:	#only reset if it is set
					self.__solarSupply = False

