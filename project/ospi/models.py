from django.contrib.auth.models import User
from django.db import models


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

    def __unicode__(self):
        return u"%s" % self.user


class Day(models.Model):
    day = models.CharField(max_length=10)

    def __unicode(self):
        return self.day


class Station(models.Model):
    account = models.ForeignKey(Account)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    pump = models.BooleanField(default=False)
    heads = models.IntegerField(default=0)
    soil_type = models.CharField(max_length=15, choices=SOIL_TYPES, blank=True)
    ignore_rain = models.BooleanField(default=False)


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


class Weather(models.Model):
    day = models.DateField()
    high = models.IntegerField()
    low = models.IntegerField()
    rain = models.FloatField()
    humidity = models.FloatField()

    def __unicode__(self):
        return "%s (%s, %s)" % (self.day, self.low, self.high)
