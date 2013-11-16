from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class HomeView(DetailView):
    template_name = 'ospi/rpi_home.html'

    def get_object(self, queryset=None):
        return []

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['stations'] = Station.objects.all()
        return context


class StationsListView(ListView):
    template_name='ospi/stations_view.html'
    model=Station


class CreateStationsView(CreateView):
    template_name='ospi/station_create.html'
    model=Station

    def get_success_url(self):
        return reverse('stations_list')


class UpdateStationsView(UpdateView):
    template_name='ospi/stations_edit.html'
    model=Station

    def get_success_url(self):
        return reverse('stations_list')


class ScheduleListView(ListView):
    template_name='ospi/schedule_list.html'
    model=Schedule


class CreateScheduleView(CreateView):
    template_name='ospi/schedule_create.html'
    model=Schedule

    def get_success_url(self):
        return reverse('schedule_list')


class CreateAccountView(CreateView):
    template_name='ospi/account_create.html'
    model=Account
    def get_success_url(self):
        return reverse('home')


class WaterLogView(ListView):
    template_name='ospi/waterlog_view.html'
    model=WaterLog
