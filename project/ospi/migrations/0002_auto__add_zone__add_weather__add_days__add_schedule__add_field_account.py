# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zone'
        db.create_table(u'ospi_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pump', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('heads', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('soil_type', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
        ))
        db.send_create_signal(u'ospi', ['Zone'])

        # Adding model 'Weather'
        db.create_table(u'ospi_weather', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('high', self.gf('django.db.models.fields.IntegerField')()),
            ('low', self.gf('django.db.models.fields.IntegerField')()),
            ('rain', self.gf('django.db.models.fields.FloatField')()),
            ('humidity', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'ospi', ['Weather'])

        # Adding model 'Days'
        db.create_table(u'ospi_days', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'ospi', ['Days'])

        # Adding model 'Schedule'
        db.create_table(u'ospi_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('day_restrictions', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('interval', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('repeat', self.gf('django.db.models.fields.TimeField')()),
            ('run_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'ospi', ['Schedule'])

        # Adding M2M table for field days on 'Schedule'
        m2m_table_name = db.shorten_name(u'ospi_schedule_days')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'ospi.schedule'], null=False)),
            ('days', models.ForeignKey(orm[u'ospi.days'], null=False))
        ))
        db.create_unique(m2m_table_name, ['schedule_id', 'days_id'])

        # Adding M2M table for field zones on 'Schedule'
        m2m_table_name = db.shorten_name(u'ospi_schedule_zones')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'ospi.schedule'], null=False)),
            ('zone', models.ForeignKey(orm[u'ospi.zone'], null=False))
        ))
        db.create_unique(m2m_table_name, ['schedule_id', 'zone_id'])

        # Adding field 'Account.weather_api'
        db.add_column(u'ospi_account', 'weather_api',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Account.zip_code'
        db.add_column(u'ospi_account', 'zip_code',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Zone'
        db.delete_table(u'ospi_zone')

        # Deleting model 'Weather'
        db.delete_table(u'ospi_weather')

        # Deleting model 'Days'
        db.delete_table(u'ospi_days')

        # Deleting model 'Schedule'
        db.delete_table(u'ospi_schedule')

        # Removing M2M table for field days on 'Schedule'
        db.delete_table(db.shorten_name(u'ospi_schedule_days'))

        # Removing M2M table for field zones on 'Schedule'
        db.delete_table(db.shorten_name(u'ospi_schedule_zones'))

        # Deleting field 'Account.weather_api'
        db.delete_column(u'ospi_account', 'weather_api')

        # Deleting field 'Account.zip_code'
        db.delete_column(u'ospi_account', 'zip_code')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '8080'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'weather_api': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ospi.days': {
            'Meta': {'object_name': 'Days'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ospi.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'day_restrictions': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ospi.Days']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repeat': ('django.db.models.fields.TimeField', [], {}),
            'run_time': ('django.db.models.fields.TimeField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'zones': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ospi.Zone']", 'symmetrical': 'False'})
        },
        u'ospi.weather': {
            'Meta': {'object_name': 'Weather'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'high': ('django.db.models.fields.IntegerField', [], {}),
            'humidity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.IntegerField', [], {}),
            'rain': ('django.db.models.fields.FloatField', [], {})
        },
        u'ospi.zone': {
            'Meta': {'object_name': 'Zone'},
            'heads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pump': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'soil_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['ospi']