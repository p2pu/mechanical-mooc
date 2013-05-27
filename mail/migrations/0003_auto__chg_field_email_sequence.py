# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Email.sequence'
        db.alter_column('mail_email', 'sequence', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'Email.sequence'
        db.alter_column('mail_email', 'sequence', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'mail.email': {
            'Meta': {'object_name': 'Email'},
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_scheduled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'html_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '78'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'text_body': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mail']