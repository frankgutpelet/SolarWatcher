import threading
import time

class VictronReader:
    __instance = None

    def GetInstance():
        if (VictronReader.__instance == None):
            return VictronReader()
        return VictronReader.__instance

    def __init__(self):
        if VictronReader.__instance != None:
            raise Exception("This class is a singleton")
        else:
            VictronReader.__instance = self

        self.batV = 0
        self.solV = 0
        self.batI = 0
        self.supply = "unknown"
        self.chargemode = "unknown"
        self.devices = list()

        self.VictronThread = threading.Thread(target=self.ReadVictronValues, args=())
        self.VictronThread.start()

    def ReadVictronValues(self):
        path = "/tmp/solarWatcher.fifo"
        values = []

        while True:
            fifo = open(path, "r")
            for line in fifo:
                values = line.split(';')
            if len(values) >= 5:
                self.batV = values[0]
                self.batI = values[1]
                self.solV = values[2]
                self.supply = values[3]
                self.chargemode = values[4]
            self.devices.clear()
            for index in range(5, len(values), 2):
                if len(values) < (index + 2):
                    break
                self.devices.append({'name' : values[index], 'value' : values[index + 1]})
            fifo.close()
            time.sleep(1)
