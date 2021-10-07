import threading
import time


class VictronReader:
    __instance = None
    batteries = list()

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
        self.temp = 0
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
            if len(values) >= 1 and 'Battery' == values[0]:
                self.parseBattery(values)
            elif len(values) >= 5:
                self.batV = values[0]
                self.batI = values[1]
                self.solV = values[2]
                self.supply = values[3]
                self.chargemode = values[4]
                self.temp = values[5]
            self.devices.clear()
            for index in range(6, len(values), 3):
                if len(values) < (index + 3):
                    break
                self.devices.append({'name' : values[index], 'value' : values[index + 1], 'frostschutz' : values[index + 2]})
            fifo.close()
            time.sleep(1)

    def parseBattery(self, values):
        battery = None
        for bat in self.batteries:
            if values[1] == bat['number']:
                bat['name'] = values[2]
                bat['v1'] = values[3]
                bat['v2'] = values[4]
                bat['I'] = values[5]
                bat['warning'] = values[6]
                return

        battery = dict()
        battery['number'] = values[1]
        battery['name'] = values[2]
        battery['v1'] = values[3]
        battery['v2'] = values[4]
        battery['I'] = values[5]
        battery['warning'] = values[6]
        self.batteries.append(battery)


