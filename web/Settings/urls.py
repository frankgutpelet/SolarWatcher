from django.urls import path
from . import views

app_name = 'Settings'

urlpatterns = [
    path('', views.index, name='index'),
]

