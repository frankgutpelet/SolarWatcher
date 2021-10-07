import serial
import re

class ADC(object):
    com : serial.Serial
    number : int

    def __init__(self, number : int, tty : str):
        self.tty = tty
        self.com = serial.Serial(tty, 115200)
        self.number = number

    def getValues(self):
        self.com.flush()
        finish = False
        voltage = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
        while(not finish):
            line = str(self.com.readline())

            match = re.search("(\d):\d+.+(\d+\.\d+)", line ) #"b\'CH(\d+):\d+\\t(\d+\.\d+)V\\r\\n", line)
            if match:
                values = match.groups()
                index = int(values[0])
                voltage[index] = float(values[1])
                finish = True
                for result in voltage:
                    if -1.0 == result:
                        finish = False



        return voltage