import datetime
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import *


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


def enable_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        try:
            station.enable()
            return \
                HttpResponse(
                    """{"status": 200}""",
                    content_type="application/json"
                )
        except Exception as e:
            logging.error(e)
            return \
                HttpResponse(
                    """{"status": 500}""",
                    content_type="application/json",
                    status=500
                )

def disable_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        try:
            station.disable()
            return \
                HttpResponse(
                    """{"status": 200}""",
                    content_type="application/json"
                )
        except Exception as e:
            logging.error(e)
            return \
                HttpResponse(
                    """{"status": 500}""",
                    content_type="application/json",
                    status=500
                )


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
        pie = []
        data.append(['Day','Usage'])
        pie.append(['Station', 'Total Hours'])
        total = 0.0
        for i in range(0,31):
            time_running = 0.0
            time = timezone.now()-datetime.timedelta(days=30-i)
            logs = WaterLog.objects.filter(start_time__gte=time, start_time__lt=time+datetime.timedelta(days=1))
            for log in logs:
                running = log.length.days * 24 + log.length.seconds // 3600
                time_running += running*log.station.heads

            usage = time_running*5
            total += usage
            data.append([(str(time.month)+'/'+str(time.day)), round(usage,2)])

        for station in Station.objects.all():
            logs = WaterLog.objects.filter(start_time__gte=timezone.now()-datetime.timedelta(days=30), station=station)
            head_usage = 0
            for log in logs:
                head_usage += (log.length.days * 24 + log.length.seconds //3600) * log.station.heads
            pie.append([str(station.name), head_usage])
        
        context['data'] = data
        context['total'] = round(total,2)
        context['pie'] = pie
        return context
