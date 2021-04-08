from django.urls import path
from . import views

app_name = 'Rikatronic'

urlpatterns = [
    path('', views.index, name='index'),
    path('setValues', views.setValues, name='setValues'),
    path('getValues', views.getValues, name='getValues'),
    path('power', views.power, name='power'),
    path('manual', views.manual, name='manual'),
    path('eco', views.eco, name='eco'),
    path('flap', views.flap, name='flap'),
]