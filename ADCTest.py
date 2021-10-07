from ADC import ADC

adc1 = ADC("/dev/ttyUSB1")

values = adc1.getValues()
for value in values:
    print("CH" + str(values.index(value)) + ": " + str(value) + "V\n")