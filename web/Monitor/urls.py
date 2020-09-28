from django.urls import path
from . import views

app_name = 'Monitor'

urlpatterns = [
    path('', views.index, name='index'),
]