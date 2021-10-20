import xml.etree.ElementTree as ET

class Switch(object):
    def __init__(self, config):
        self.id = config.attrib['id']
        self.enable = config.attrib['enable']
        self.supply = config.attrib['supply']
        self.voltage = config.attrib['voltage']
        self.on = config.attrib['on']
        self.off = config.attrib['off']
        if 'frostschutz' in config.attrib:
            self.frostschutz = config.attrib['frostschutz']
        else:
            self.frostschutz = None

class Release(object):
    def __init__(self, config):
        self.number = config.attrib['number']
        self.name = config.attrib['name']
        self.prio = config.attrib['prio']
        self.maxpower = config.attrib['maxpower']
        self.switches = list()

        for switch in config.findall('Switch'):
            self.switches.append(Switch(switch))



class Configuration(object):
    def __init__(self):
        self.configfile = ET.parse("../Releases.xml")
        self.root = self.configfile.getroot()
        self.releases = list()
        self.loglevel = self.root.find('Logging').attrib['loglevel']
        self.logToCsv = self.root.find('Logging').attrib['cvs']

        for release in self.root.findall('Release'):
            self.releases.append(Release(release))


    def setLoglevel(self, loglevel):
        self.loglevel = loglevel
        self.root.find('Logging').attrib['loglevel'] = loglevel
        self.configfile.write("../Releases.xml", xml_declaration=True, encoding = "UTF-8")

    def setCsv(self, csv):
        self.logToCsv = csv
        self.root.find('Logging').attrib['cvs'] = csv
        self.configfile.write("../Releases.xml", xml_declaration=True, encoding="UTF-8")

    def setMode(self, device, mode):
        device = device.split(' [')[0]
        for child in self.root:
            if 'name' in child.attrib and device == child.attrib['name']:
                child.attrib['mode'] = mode
                self.configfile.write("../Releases.xml", xml_declaration=True, encoding="UTF-8")
                return


