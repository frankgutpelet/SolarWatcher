import serial
import mylogging
import datetime
import threading
import os
import time 
import FrontendInterface
import traceback

class Victron(object):
	"""this class reads state of the victron energy charger and controls it"""

	class Error:
		No_error=0
		Battery_voltage_too_high=2
		Charger_temperature_too_high=17
		Charger_over_current=18
		Charger_current_reversed=19
		Bulk_time_limit_exceeded=20
		Current_sensor_issue_sensor_bias_sensor_broken=21
		Terminals_overheated=26
		Input_voltage_too_high_solar_panel=33
		Input_current_too_high_solar_panel=34
		Input_shutdown_due_to_excessive_battery_voltage=38
		Factory_calibration_data_lost=116
		Invalid_incompatible_firmware=117
		User_settings_invalid=119

		def getError(errorcode):
			if (Victron.Error.No_error==errorcode):
				return "No_error"
			elif (Victron.Error.Battery_voltage_too_high==errorcode):
				return "Battery_voltage_too_high"
			elif (Victron.Error.Charger_temperature_too_high==errorcode):
				return "Charger_temperature_too_high"
			elif (Victron.Error.Charger_over_current==errorcode):
				return "Charger_over_current"
			elif (Victron.Error.Charger_current_reversed==errorcode):
				return "Charger_current_reversed"
			elif (Victron.Error.Bulk_time_limit_exceeded==errorcode):
				return "Bulk_time_limit_exceeded"
			elif (Victron.Error.Current_sensor_issue_sensor_bias_sensor_broken==errorcode):
				return "Current_sensor_issue_sensor_bias_sensor_broken"
			elif (Victron.Error.Terminals_overheated==errorcode):
				return "Terminals_overheated"
			elif (Victron.Error.Input_voltage_too_high_solar_panel==errorcode):
				return "Input_voltage_too_high_solar_panel"
			elif (Victron.Error.Input_current_too_high_solar_panel==errorcode):
				return "Input_current_too_high_solar_panel"
			elif (Victron.Error.Input_shutdown_due_to_excessive_battery_voltage==errorcode):
				return "Input_shutdown_due_to_excessive_battery_voltage"
			elif (Victron.Error.Factory_calibration_data_lost==errorcode):
				return "Factory_calibration_data_lost"
			elif (Victron.Error.Invalid_incompatible_firmware==errorcode):
				return "Invalid_incompatible_firmware"
			else:
				return "unknown Error Errorcode: " + str(errorcode)

	class ChargingState:
		Off=0
		Low_power=1
		Fault=2
		Bulk=3
		Absorption=4
		Float=5
		Inverting=9

		def GetState(state):
			if Victron.ChargingState.Off==state:
				return "Off"
			elif Victron.ChargingState.Low_power==state:
				return "Low Power"
			elif Victron.ChargingState.Fault==state:
				return "Fault"
			elif Victron.ChargingState.Bulk==state:
				return "Bulk"
			elif Victron.ChargingState.Absorption==state:
				return "Absorption"
			elif Victron.ChargingState.Float==state:
				return "Float"
			elif Victron.ChargingState.Inverting==state:
				return "Inverting"
			else:
				return "Unknown state " + str(state)


	def __init__(self, solarSupply, logger, comport, watchdog):
		self.logger = logger
		self.Connect(comport)
		self.solarSupply = solarSupply
		self.batVoltage = 0
		self.pipeLength = 0
		self.wdIndex = watchdog.subscribe("Victron", 2)
		self.watchdog = watchdog
		self.FrontendIf = FrontendInterface.FrontEnd.GetInstance(logger)
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
			try:
				line = ""
				self.com.flush()
				update = False
				for i in range(1, 20):

					line = str(self.com.readline())
					try:
						pair = line.split('\\r\\n')[0].split('b\'')[1].split('\\t')
					except:
						self.logger.Debug("could not parse: " + line)
						continue

					if 2 > len(pair):
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
					elif ('CS' == pair[0]):
						self.mode = int(pair[1])
						if (mod != self.mode):
							mod = self.mode
					elif ('ERR' == pair[0]):
						self.errorcode = int(pair[1])
						if(Victron.Error.No_error != self.errorcode):
							self.logger.Error(Victron.Error.getError(self.errorcode))

				if(self.solarSupply.SolarSupply()):
					self.FrontendIf.updateVictronData(batV, cur, solV, Victron.ChargingState.GetState(mod), "Solar")
				else:
					self.FrontendIf.updateVictronData(batV, cur, solV, Victron.ChargingState.GetState(mod), "Netz")
				self.FrontendIf.sendData()

				if update:
					self.logger.ToCVS(batV, solV, Victron.ChargingState.GetState(mod), cur, self.solarSupply.SolarSupply())
				time.sleep(1)
			except Exception  as e:
				self.logger.Error("Error in Victron Thread " + str(e) + " in line: " + line + traceback.format_exc())

			self.watchdog.trigger(self.wdIndex)


