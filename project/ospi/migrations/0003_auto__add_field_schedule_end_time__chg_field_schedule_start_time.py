# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Schedule.end_time'
        db.add_column(u'ospi_schedule', 'end_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.time(0, 0)),
                      keep_default=False)


        # Changing field 'Schedule.start_time'
        db.alter_column(u'ospi_schedule', 'start_time', self.gf('django.db.models.fields.TimeField')())

    def backwards(self, orm):
        # Deleting field 'Schedule.end_time'
        db.delete_column(u'ospi_schedule', 'end_time')


        # Changing field 'Schedule.start_time'
        db.alter_column(u'ospi_schedule', 'start_time', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ospi.account': {
            'Meta': {'object_name': 'Account'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "'opendoor'", 'max_length': '100', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '8080'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'weather_api': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ospi.day': {
            'Meta': {'object_name': 'Day'},
            'bit_value': ('django.db.models.fields.IntegerField', [], {'default': '1', 'unique': 'True'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ospi.forecastweather': {
            'Meta': {'object_name': 'ForecastWeather'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'high': ('django.db.models.fields.IntegerField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.IntegerField', [], {}),
            'rain': ('django.db.models.fields.FloatField', [], {})
        },
        u'ospi.hourlyweather': {
            'Meta': {'object_name': 'HourlyWeather'},
            'hour': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rain': ('django.db.models.fields.FloatField', [], {}),
            'temperature': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ospi.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ospi.Account']"}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'day_restrictions': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'schedules'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ospi.Day']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'interval_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repeat': ('django.db.models.fields.TimeField', [], {}),
            'run_time': ('django.db.models.fields.TimeField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'stations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ospi.Station']", 'symmetrical': 'False'})
        },
        u'ospi.station': {
            'Meta': {'unique_together': "(('account', 'number'),)", 'object_name': 'Station'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stations'", 'to': u"orm['ospi.Account']"}),
            'heads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_rain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pump': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'soil_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'ospi.waterlog': {
            'Meta': {'object_name': 'WaterLog'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ospi.Account']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ospi.Schedule']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ospi.Station']"})
        }
    }

    complete_apps = ['ospi']