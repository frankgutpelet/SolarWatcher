import threading
import os
import xml.etree.ElementTree as ET
from BatteryString import BatteryString
from ADC import ADC
import logging
from FrontendInterface import FrontEnd
import time

class FuelGauge(object):
    strings = list()
    adcs = list()
    logger : logging
    configTimestamp = 0

    def __init__(self, configfile, logger : logging):
        self.logger = logger
        self.configfile = configfile
        self.FrontEndInterface = FrontEnd.GetInstance(logger)
        self.__parseConfig()
        self.configTimestamp = os.path.getmtime(self.configfile)
        self.FuelGaugeThread = threading.Thread(target=self.__FuelGaugeThread, args=())
        #self.FuelGaugeThread.start()


    def __FuelGaugeThread(self):
        self.logger.Error("FuelGauge Started")
        while True:

            if self.configTimestamp != os.path.getmtime(self.configfile):
                self.configTimestamp = os.path.getmtime(self.configfile)
                self.__parseConfig()

            for string in self.strings:
                string.getValues()
                self.FrontEndInterface.updateBattery(string.name, string.number, round(string.voltage1, 2), round(string.voltage2, 2), round(string.current, 2), "")

            time.sleep(5)


    def __parseConfig(self):
        try:
            config = ET.parse(self.configfile)
        except Exception:
            self.logger.Error("Battery configfile not valid xml")
            return
        root = config.getroot()

        self.strings.clear()
        self.adcs.clear()

        for adcelem in root.findall('ADC'):
            self.adcs.append(ADC(int(adcelem.attrib['number']), adcelem.attrib['tty']))
            self.logger.Error("found new ADC: " + adcelem.attrib['number'])

        for string in root.findall('String'):
            adcnumber = int(string.attrib['ADC'])
            currentChannel = int(string.attrib['channel'])
            name = string.attrib['name']
            number = int(string.attrib['number'])
            bat1Channel = int(string.find("Battery1").attrib['channel'])
            bat2Channel = int(string.find("Battery2").attrib['channel'])
            for adc in self.adcs:
                if adcnumber == adc.number:
                    self.strings.append(BatteryString(self.logger, number, name, adc, bat1Channel, bat2Channel, currentChannel))
                    self.logger.Error("found new Batterystring: " + name)


