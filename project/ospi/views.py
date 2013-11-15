from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, ListView, UpdateView

# Create your views here.
class CreateZoneView(CreateView):
    template_name='ospi/zone_create.html'
    model=Zone

class CreateScheduleView(CreateView):
    template_name='ospi/schedule_create.html'
    model=Schedule
