from django.shortcuts import render
import os
from html import unescape
from django.http import JsonResponse
import VictronReader


# Create your views here.


def index(request):

    reader = VictronReader.VictronReader.GetInstance()
    table = "<tbody><tr>\n" + \
       "<td class=\"auto-style2\" style=\"width: 84px\"><strong>String</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>Name</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>Voltage</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>Cell 1</strong></td>\n" + \
        "<td class=\"auto-style2\"><strong>Cell 2</strong></td>\n" + \
        "<td class=\"auto-style2\"><strong>Current</strong></td>\n" + \
        "</tr></tbody>"

    for battery in reader.batteries:
        table += "<tr>\n" + \
       "<td class=\"auto-style2\" style=\"width: 84px\"><strong>" + battery['number'] + "</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>" + battery['name'] + "</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>" + str(round((float(battery['v1']) + float(battery['v2'])),2) ) + "V</strong></td>\n" + \
       "<td class=\"auto-style2\"><strong>" + battery['v1'] + "V</strong></td>\n" + \
        "<td class=\"auto-style2\"><strong>" + battery['v2'] + "V</strong></td>\n" + \
        "<td class=\"auto-style2\"><strong>" + battery['I'] + "A</strong></td>\n" + \
        "</tr>"

    return render(request, 'Battery/base.html',
              {'batteryTable': table})

