import serial
import mylogging
import datetime

class Victron(object):
	"""this class reads state of the victron energy charger and controls it"""

	def __init__(self, solarSupply, logger, comport):
		self.Connect(comport)
		self.logger = loggerange
		self.solarSupply = solarSupply
		self.ReadThread = threading.Thread(target=self.__ReadThread, args = ())
		return 

	def Connect(self, comport):
		self.com = serial.Serial(comport, 19200)

	def Disconnect(self):
		if self.com.isOpen():
			self.com.close()

	def __ReadThread(self):

		while True:
			ser.flush()
			batV=0
			solV=0
			cur=0
			mod=0
			for i in range(1, 20):
				line = str(ser.readline())
				try:
					pair = line.split('\\r\\n')[0].split('b\'')[1].split('\\t')
				except IndexError:
					self.logger.Error("Error cannot parse text: " + line)
					return
		
				if ('V' == pair[0]):
					batV = self.batVoltage = int(pair[1])/1000
				elif ('VPV' == pair[0]):
					solV = self.solVoltage = int(pair[1])/1000
				elif ('I' == pair[0]):
					cur = self.chargeCur = int(pair[1])/1000
				elif ('MPPT' == pair[0]):
					mod = self.mode = int(pair[1])/1000

				self.logger.ToCVS(batV, solV, mod, cur, self.solarSupply.SolarSupply())

