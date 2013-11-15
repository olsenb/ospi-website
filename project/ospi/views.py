from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, ListView, UpdateView

# Create your views here.
class CreateStationsView(CreateView):
    template_name='ospi/station_create.html'
    model=Station

class CreateScheduleView(CreateView):
    template_name='ospi/schedule_create.html'
    model=Schedule
