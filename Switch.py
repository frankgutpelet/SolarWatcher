from datetime import datetime

class switch:
    SUPPLY_MAINS = 0
    SUPPLY_SOLAR = 1
    SUPPLY_ALL = 2

    no : int
    hourOn : int
    minuteOn : int
    hourOff : int
    minuteOff : int
    name : str
    voltage : float
    prio : int
    maxpower : int
    isOn : bool
    switchNumber : int
    supply = int
    tempMin : float
    tempProtection : bool
    mode : str
    minimumRuntimeMinPerDay : int  # configured by releases
    minRuntimeForce : bool      # force flag that forces over all
    lastSyncAbsMinute : int     # timestamp for the last update of runtime
    doneTimeAbsMinute : int     #counter for runtime on current day
    resetDay : int

    def __init__(self, No, ontime, offtime, voltage, name, prio, maxpower, supply, tempMin, mode, logging, minimumRuntime = 0):
        self.no = No
        self.hourOn = int(ontime.split(":")[0])
        self.minuteOn = int(ontime.split(":")[1])
        self.hourOff = int(offtime.split(":")[0])
        self.minuteOff = int(offtime.split(":")[1])
        self.name = name
        self.voltage = float(voltage)
        self.prio = int(prio)
        self.maxpower = int(maxpower)
        self.isOn = False
        self.switchNumber = 0
        self.supply = supply
        self.tempMin = float(tempMin)
        self.tempProtection = False
        self.mode = mode
        self.runTimeMinCurrentDay = 0
        self.minimumRuntimeMinPerDay = minimumRuntime
        self.doneTimeAbsMinute = 0
        self.resetDay = datetime.now().day
        self.logging = logging

    def Update(self, ontime, offtime, voltage, name, prio, maxpower, supply, tempMin, mode, minimumRuntime = 0):
        self.hourOn = int(ontime.split(":")[0])
        self.minuteOn = int(ontime.split(":")[1])
        self.hourOff = int(offtime.split(":")[0])
        self.minuteOff = int(offtime.split(":")[1])
        self.name = name
        self.voltage = float(voltage)
        self.prio = int(prio)
        self.maxpower = int(maxpower)
        self.switchNumber = 0
        self.supply = supply
        self.tempMin = float(tempMin)
        self.tempProtection = False
        self.mode = mode
        self.minimumRuntimeMinPerDay = minimumRuntime

    def CheckTime(self):
        if self.resetDay != datetime.now().day:
            self.logging.Error("reset timer for " + self.name + " switched on today for " + str(self.doneTimeAbsMinute) + "minutes")
            self.doneTimeAbsMinute = 0
            self.resetDay = datetime.now().day
