import xml.etree.ElementTree as ET

class switch:
	SUPPLY_MAINS = 0
	SUPPLY_SOLAR = 1
	SUPPLY_ALL = 2

	def __init__(self, No, ontime, offtime, voltage, name, prio, maxpower, supply, id):
		self.no = No
		self.hourOn = int(ontime.split(":")[0])
		self.minuteOn = int(ontime.split(":")[1])
		self.hourOff = int(offtime.split(":")[0])
		self.minuteOff = int(offtime.split(":")[1])
		self.name = name
		self.voltage = float(voltage)
		self.prio = int(prio)
		self.maxpower = int(maxpower)
		self.supply = supply
        self.id = id

class Configuration(object):
    __path__ = "../../Releases.xml"
    ATTRIB_ENABLE = "enable"

    def __init__(self):
        self.readFile()
        self.switches = list()

    def writeAttrib(self, switch, attrib, value):
        root = self.config.getroot()
        updated = False

        for release in root.findall('Release'):
            no = int(release.attrib['number'])
            for cur_switch in release.findall('Switch'):
                id = no * 10 + int(cur_switch.attrib['id'])
                if(id == switch.id):
                    cur_switch.attrib[attrib] = value
                    update = True
    if update:
        self.config.write(self.__path__)



    def readFile(self):
        try:
            self.config = ET.parse(self.configfile)
        except Exception:
            self.logger.Error("configfile not valid xml")
            return
        root = self.config.getroot()

        for release in root.findall('Release'):

            no = release.attrib['number']
            name = release.attrib['name']
            prio = release.attrib['prio']
            maxpower = release.attrib['maxpower']


            for cur_switch in release.findall('Switch'):
                if "solar" == cur_switch.attrib['supply']:
                    supply = switch.SUPPLY_SOLAR
                elif "all" == cur_switch.attrib['supply']:
                    supply = switch.SUPPLY_ALL
                elif "mains" == cur_switch.attrib['supply']:
                    supply = switch.SUPPLY_MAINS

                if "False" == cur_switch.attrib['enable']:
                    enable = False
                else:
                    enable = True
                id = int(no)*10 + int(cur_switch.attrib['id'])
                new_switch = switch(no, cur_switch.attrib['on'], cur_switch.attrib['off'],
                                        cur_switch.attrib['voltage'], name, prio, maxpower, supply, id)

                self.switches.append(new_switch)

        self.logger.Debug("Release Configuration updated successful")