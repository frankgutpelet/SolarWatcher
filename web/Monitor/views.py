from django.shortcuts import render
import VictronReader
from html import unescape
from Settings.Configuration import Configuration

victronReader = VictronReader.VictronReader.GetInstance()
# Create your views here.

def makeTableEntry(key, value, frostschutz):
    if "False" in frostschutz:
        return "<tr>\n" + \
        "<td class=\"auto-style2\" style=\"width: 484px\"><strong>" + key + "</strong></td>\n" + \
        "<td class=\"auto-style2\"><strong>" + value + "</strong></td>\n" + \
        "<td> <form action=\"/Monitor\" method=\"GET\"> <input type=\"hidden\" name=\"mode\" id=\"mode\" value=\"ON\"> <input type=\"hidden\" name=\"device\" id=\"device\" value=\"" + key + "\"> <input type=\"submit\" value=\"ON\"> </form> </td>\n" + \
        "<td> <form action=\"/Monitor\" method=\"GET\"> <input type=\"hidden\" name=\"mode\" id=\"mode\" value=\"AUTO\"> <input type=\"hidden\" name=\"device\" id=\"device\" value=\"" + key + "\"> <input type=\"submit\" value=\"AUTO\"> </form> </td>\n" + \
        "<td> <form action=\"/Monitor\" method=\"GET\"> <input type=\"hidden\" name=\"mode\" id=\"mode\" value=\"OFF\"> <input type=\"hidden\" name=\"device\" id=\"device\" value=\"" + key + "\"> <input type=\"submit\" value=\"OFF\"> </form> </td>\n" + \
        "</tr>"
    else:
        return "<tr>\n" + \
       "<td class=\"auto-style2\" style=\"width: 484px\"><strong>" + key + "</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>" + value + " (Frostschutz)</strong></td>\n" + \
       "</tr>"

def index(request):
    global victronReader

    deviceTable = str()

    if 'mode' in request.GET:
        config = Configuration()
        config.setMode(request.GET['device'], request.GET['mode'])

    for device in victronReader.devices:
        deviceTable += makeTableEntry(device['name'], device['value'], device['frostschutz'])

    return render(request, 'Monitor/base.html',
                      {'batV': victronReader.batV, 'batI': victronReader.batI, 'solV': victronReader.solV,
                       'solarSupply': victronReader.supply, 'chargingState': victronReader.chargemode,
                       'solarPower': str(round(float(victronReader.batV) * float(victronReader.batI))), 'aussentemp' : victronReader.temp,
                       'deviceTable': unescape(deviceTable)})