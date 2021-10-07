from ADC import ADC
from mylogging import Logging

class BatteryString(object):

    name : str
    number : int
    adc : ADC
    portU1 : int
    portU2 : int
    portI : int
    voltage1 : float
    voltage2 : float
    voltage : float
    current : float
    voltageFactor1 = 5.7
    voltageFactor2 = 11
    currentFactor = 15.1515
    currentOffset = 2.545



    def __init__(self, logger : Logging, number : int, name : str, adc : ADC, portU1, portU2, portI):
        self.adc = adc
        self.portU1 = portU1
        self.portU2 = portU2
        self.portI = portI
        self.number = number
        self.name = name
        self.logger = logger
        self.getValues()

    def getValues(self):
        adcValues = self.adc.getValues()
        self.voltage1 = adcValues[self.portU1] * self.voltageFactor1
        self.voltage2 = (adcValues[self.portU2] * self.voltageFactor2) - self.voltage1
        self.voltage = self.voltage1 + self.voltage2
        self.current = -((adcValues[self.portI] - self.currentOffset) * self.currentFactor)

        self.logger.Debug("current adc value: " + str(adcValues[self.portI]))
        self.logger.Debug("current: " + str(self.current) + "A")
        self.logger.Debug("v1 adc value: " + str(adcValues[self.portU1]))
        self.logger.Debug("v1: " + str(self.voltage1) + "A")
        self.logger.Debug("v2 adc value: " + str(adcValues[self.portU2]))
        self.logger.Debug("v2: " + str(self.voltage2) + "A")