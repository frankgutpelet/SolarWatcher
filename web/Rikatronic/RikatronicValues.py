import threading
import time
import datetime

class RicatronicValues:
    __instance = None

    PROGRAM_NONE = "kalt"
    PROGRAM_HEAT_UP = "anheizen"
    PROGRAM_TROTTLE = "heiß"
    PROGRAM_ECO = "eco"

    MODE_ECO = 'ECO'
    MODE_POWER = 'POWER'
    MODE_MANUAL = 'MANUAL'

    def GetInstance():
        if (RicatronicValues.__instance == None):
            return RicatronicValues()
        return RicatronicValues.__instance

    def __init__(self):
        if RicatronicValues.__instance != None:
            raise Exception("This class is a singleton")
        else:
            RicatronicValues.__instance = self

        self.ofentemp = 0
        self.program = RicatronicValues.PROGRAM_NONE
        self.time_hours = 0
        self.time_minutes = 0
        self.flap = 0
        self.mode = RicatronicValues.MODE_ECO
        self.__heatUpTimestamp = datetime.datetime.now()

    def UpdateValues(self, program, flap, ofentemp):

        if(     (RicatronicValues.PROGRAM_NONE == self.program)
            and (RicatronicValues.PROGRAM_HEAT_UP == program)):
            self.__heatUpTimestamp = datetime.datetime.now()

        self.flap = int(flap)
        self.program = program
        self.ofentemp = int(ofentemp)

    def getTime (self):
        timedif = datetime.datetime.now() - self.__heatUpTimestamp
        hours = int(timedif.total_seconds() / 3600)
        minutes = int((timedif.total_seconds() - (hours * 3600)) /60)
        return hours, minutes



