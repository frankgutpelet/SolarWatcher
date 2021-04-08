from django.shortcuts import render
import os
from . import VictronReader
from html import unescape
from . import Configuration

# Create your views here.

def makeReleaseEntry(release, prio, power, number):
    return "<tr>\n" + \
    "<td class=\"auto-style2\" style=\"width: 484px\"><strong>" + release + "</strong></td>\n" + \
    "<td class=\"auto-style2\"><strong>Prio " + prio + "</strong></td>\n" + \
    "<td class=\"auto-style2\"><strong>" + power + "W</strong></td>\n" + \
    "<td class=\"auto-style2\"><strong>Solarfreigabe_" + number + "</strong></td>\n" + \
    "</tr>"
def makeSwitchEntry(enable, supply, voltage, on, off, frostschutz):
    if None != frostschutz:
        return "<tr>\n" + \
       "<td class=\"auto-style3\" style=\"width: 484px\"><strong>" + enable + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + supply + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + voltage + "V</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + on + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + off + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + frostschutz + "°C</strong></td>\n" + \
       "</tr>"
    else:
        return "<tr>\n" + \
       "<td class=\"auto-style3\" style=\"width: 484px\"><strong>" + enable + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + supply + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + voltage + "V</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + on + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>" + off + "</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong></strong></td>\n" + \
       "</tr>"

def createLoggingDropdown(loglevel):

    if "DEBUG" == loglevel:
        return "<option value = \"DEBUG\" > DEBUG </option>\n" + \
        "<option value = \"INFO\" > INFO </option>\n" + \
        "<option value = \"ERROR\" > ERROR </option>\n"
    if "INFO" == loglevel:
        return "<option value = \"INFO\" > INFO </option>\n" + \
        "<option value = \"DEBUG\" > DEBUG </option>\n" + \
        "<option value = \"ERROR\" > ERROR </option>\n"
    if "ERROR" == loglevel:
        return "<option value = \"ERROR\" > ERROR </option>\n" + \
        "<option value = \"INFO\" > INFO </option>\n" + \
        "<option value = \"DEBUG\" > DEBUG </option>\n"

def createCsvDropdown(csv):

    if "True" == csv:
        return "<option value = \"True\" > True </option>\n" + \
        "<option value = \"False\" > False </option>\n"
    if "False" == csv:
        return "<option value = \"False\" > False </option>\n" + \
        "<option value = \"True\" > True </option>\n"



def index(request):

    config = Configuration.Configuration()

    if 'loglevel' in request.GET:
        config.setLoglevel(request.GET['loglevel'])
    if 'csv' in request.GET:
        config.setCsv(request.GET['csv'])

    deviceTable = "<tr>\n" + \
       "<td class=\"auto-style3\" style=\"width: 484px\"><strong>Aktiviert</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>Quelle</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>Batteriespannung</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>Start</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>Ende</strong></td>\n" + \
       "<td class=\"auto-style3\"><strong>Frostschutz</strong></td>\n" + \
       "</tr>"
    for release in config.releases:
        deviceTable += makeReleaseEntry(release.name, release.prio, release.maxpower, release.number)
        for switch in release.switches:
            deviceTable += makeSwitchEntry(switch.enable, switch.supply, switch.voltage, switch.on, switch.off, switch.frostschutz)

    return render(request, 'Settings/base.html',
                      {'logging': createLoggingDropdown(config.loglevel), 'csv': createCsvDropdown(config.logToCsv), 'deviceTable': unescape(deviceTable)})
