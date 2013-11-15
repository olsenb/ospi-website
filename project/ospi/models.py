from django.contrib.auth.models import User
from django.db import models
import requests


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
    #TODO: master_zone

    def get_remote_uri(self):
        #TODO: support ssl
        return "http://%s:%s" % (self.ip, self.port)

    def send(self, path, **params):
        uri = "%s/%s" % (self.get_remote_uri(), path)
        response = requests.get(uri, params=params)
        return response.text

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


class ForecastWeather(models.Model):
    day = models.DateField()
    high = models.IntegerField()
    low = models.IntegerField()
    rain = models.FloatField()
    humidity = models.FloatField()

    #manager goes here
        # it has fetch method
            # it returns a list of ForecastWeather objects

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
    station = models.ForeignKey(Station)
    program = models.ForeignKey(Schedule, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 

