import re

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import requests
from .weather import get_forecast_weather


SOIL_TYPES = (
    ('clay', 'Clay'),
    ('sand', 'Sand'),
)


DAY_TYPES = (
    (None, ''),
    (False, 'Even'),
    (True, 'Odd'),
)


class Account(models.Model):
    user = models.ForeignKey(User)
    ip = models.IPAddressField()
    port = models.IntegerField(default=8080)
    weather_api = models.CharField(max_length=100, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, default="opendoor")

    #TODO: master_zone

    def get_remote_uri(self):
        #TODO: support ssl
        return "http://%s:%s" % (self.ip, self.port)

    def send(self, path, password=False, **params):
        if password:
            params['pw'] = self.password
        uri = "%s/%s" % (self.get_remote_uri(), path)
        response = requests.get(uri, params=params)
        if response.status_code == 200:
            return response.text
        return None

    def reset_stations(self):
        self.send("cv", rsn=1, password=True)

    def get_status(self):
        #settings = self.send("")

        response = self.send("sn0")
        try:
            statuses = [bool(int(l)) for l in list(re.search("\d+", response).group(0))]
        except AttributeError:
            return None

        return {'stations': statuses}

    def __unicode__(self):
        return u"%s" % self.user


class Day(models.Model):
    day = models.CharField(max_length=10)

    def __unicode__(self):
        return self.day


class Station(models.Model):
    account = models.ForeignKey(Account)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    pump = models.BooleanField(default=False)
    heads = models.IntegerField(default=0)
    soil_type = models.CharField(max_length=15, choices=SOIL_TYPES, blank=True)
    ignore_rain = models.BooleanField(default=False)

    class Meta:
        unique_together = ('account', 'number')

    def enable(self, time=0):
        return self.account.send("sn%d=1&t=%d" % (self.number, time))

    def disable(self):
        return self.account.send("sn%d=0" % self.number)

    def status(self):
        response = self.account.send("sn%s" % self.number)
        if response is None:
            return None
        return bool(int(response))

    @property
    def short_name(self):
        return self.name[:12]

    def __unicode__(self):
        return self.name


class Schedule(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    days = models.ManyToManyField(Day, blank=True, null=True)
    day_restrictions = models.NullBooleanField(choices=DAY_TYPES)
    interval = models.IntegerField(default=1)
    start_time = models.DateTimeField()
    repeat = models.TimeField()
    run_time = models.TimeField()
    stations = models.ManyToManyField(Station)

    def __unicode__(self):
        return self.name


class ForecastWeatherManager(models.Manager):
    @staticmethod
    def fetch():
        result = get_forecast_weather()
        all_forecasts = []
        for forecast in result["forecast"]["simpleforecast"]["forecastday"]:
            day = datetime(forecast['date']['year'], forecast['date']['month'], forecast['date']['day'])
            forecast_weather = ForecastWeather(day=day, high=forecast["high"]["fahrenheit"],
                                               low=forecast["low"]["fahrenheit"], rain=forecast["qpf_allday"]["in"],
                                               humidity=forecast["minhumidity"])
            all_forecasts.append(forecast_weather)
        return all_forecasts


class ForecastWeather(models.Model):
    day = models.DateField()
    high = models.IntegerField()
    low = models.IntegerField()
    rain = models.FloatField()
    humidity = models.FloatField()

    manager = ForecastWeatherManager()

    def __unicode__(self):
        return "%s (%s, %s)" % (self.day, self.low, self.high)


class HourlyWeather(models.Model):
    hour = models.DateTimeField()
    temperature = models.IntegerField()
    rain = models.FloatField()
    humidity = models.FloatField()

    def __unicode__(self):
        return "%s %s" % (self.hour, self. temperature)


class WaterLog(models.Model):
    account = models.ForeignKey(Account)
    station = models.ForeignKey(Station)
    program = models.ForeignKey(Schedule, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    @property
    def length(self):
        return (self.end_time - self.end_time)
