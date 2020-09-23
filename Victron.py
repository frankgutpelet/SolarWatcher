import serial
import mylogging
import datetime
import threading

class Victron(object):
	"""this class reads state of the victron energy charger and controls it"""

	def __init__(self, solarSupply, logger, comport):
		self.Connect(comport)
		self.logger = logger
		self.solarSupply = solarSupply
		self.batVoltage = 0
		self.ReadThread = threading.Thread(target=self.__ReadThread, args = ())
		self.ReadThread.start()
		return 

	def Connect(self, comport):
		self.com = serial.Serial(comport, 19200)

	def Disconnect(self):
		if self.com.isOpen():
			self.com.close()

	def __ReadThread(self):
		self.logger.Debug("start Victron Thread")
		batV=0
		solV=0
		cur=0
		mod=0
		while True:
			self.com.flush()
			update = False
			for i in range(1, 20):

				line = str(self.com.readline())
				try:
					pair = line.split('\\r\\n')[0].split('b\'')[1].split('\\t')
				except IndexError:
					continue
		
				if ('V' == pair[0]):
					self.batVoltage = int(pair[1])/1000
					if (int(batV*10) != int(self.batVoltage*10)):
						batV = self.batVoltage
						update = True
				elif ('VPV' == pair[0]):
					self.solVoltage = int(pair[1])/1000
					if (int(solV/5) != int(self.solVoltage/5)):
						solV = self.solVoltage
						update = True
				elif ('I' == pair[0]):
					self.chargeCur = int(pair[1])/1000
					if (int(cur) != int(self.chargeCur)):
						cur = self.chargeCur
						update = True
				elif ('MPPT' == pair[0]):
					self.mode = int(pair[1])
					if (mod != self.mode):
						mod = self.mode
					update = True
			if update:
				self.logger.ToCVS(batV, solV, mod, cur, self.solarSupply.SolarSupply())

