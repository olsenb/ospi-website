from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.utils import timezone
import datetime


class HomeView(ListView):
    model = Account
    template_name = 'ospi/rpi_home.html'


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

class StatsView(ListView):
    template_name='ospi/rpi_stats.html'
    model=WaterLog

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        data = []
        data.append(['Day','Usage','Total'])
        total = 0.0
        for i in range(0,31):
            time_running = 0.0
            time = timezone.now()-datetime.timedelta(days=30-i)
            logs = WaterLog.objects.filter(start_time__gte=time, start_time__lt=time+datetime.timedelta(days=1))
            for log in logs:
                time_running += log.length.days * 24 + log.length.seconds // 3600

            usage = time_running*5
            total += usage

            data.append([(str(time.month) + '/' + str(time.day)), round(usage,2), round(total,2)])
        
        context['data'] = data
        return context
