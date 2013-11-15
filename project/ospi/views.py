from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, ListView, UpdateView

# Create your views here.
class StationsListView(ListView):
    model=Station

class CreateStationsView(CreateView):
    template_name='ospi/station_create.html'
    model=Station

class ScheduleListView(ListView):
    model=Schedule

class CreateScheduleView(CreateView):
    template_name='ospi/schedule_create.html'
    model=Schedule
