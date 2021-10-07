from django.urls import path
from . import views

app_name = 'Battery'

urlpatterns = [
    path('', views.index, name='index'),
]
