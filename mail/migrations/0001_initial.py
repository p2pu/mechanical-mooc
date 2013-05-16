# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table('mail_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=78)),
            ('text_body', self.gf('django.db.models.fields.TextField')()),
            ('html_body', self.gf('django.db.models.fields.TextField')()),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('date_scheduled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('mail', ['Email'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table('mail_email')


    models = {
        'mail.email': {
            'Meta': {'object_name': 'Email'},
            'date_scheduled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'html_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '78'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'text_body': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mail']