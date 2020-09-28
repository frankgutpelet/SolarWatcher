from django.shortcuts import render
import os
from . import VictronReader

# Create your views here.

def index(request):

    victronReader = VictronReader.VictronReader.GetInstance()

    return render(request, 'Monitor/base.html',
                      {'batV': victronReader.batV, 'batI': victronReader.batI, 'solV': victronReader.solV,
                       'solarSupply': victronReader.supply, 'chargingState': victronReader.chargemode,
                       'solarPower': str(round(float(victronReader.batV) * float(victronReader.batI)))})
