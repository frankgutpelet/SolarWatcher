from django.shortcuts import render
import os
from . import VictronReader
from html import unescape

# Create your views here.

def makeTableEntry(key, value):
    return "<tr>\n" + \
    "<td class=\"auto-style2\" style=\"width: 484px\"><strong>" + key + "</strong></td>\n" + \
    "<td class=\"auto-style2\"><strong>" + value + "</strong></td>\n" + \
    "</tr>"

def index(request):

    victronReader = VictronReader.VictronReader.GetInstance()
    deviceTable = str()
    for device in victronReader.devices:
        deviceTable += makeTableEntry(device['name'], device['value'])

    return render(request, 'Monitor/base.html',
                      {'batV': victronReader.batV, 'batI': victronReader.batI, 'solV': victronReader.solV,
                       'solarSupply': victronReader.supply, 'chargingState': victronReader.chargemode,
                       'solarPower': str(round(float(victronReader.batV) * float(victronReader.batI))),
                       'deviceTable': unescape(deviceTable)})
