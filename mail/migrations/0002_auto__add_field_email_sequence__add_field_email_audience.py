# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Email.sequence'
        db.add_column('mail_email', 'sequence',
                      self.gf('django.db.models.fields.CharField')(default='1', max_length=255),
                      keep_default=False)

        # Adding field 'Email.audience'
        db.add_column('mail_email', 'audience',
                      self.gf('django.db.models.fields.CharField')(default='groups', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Email.sequence'
        db.delete_column('mail_email', 'sequence')

        # Deleting field 'Email.audience'
        db.delete_column('mail_email', 'audience')


    models = {
        'mail.email': {
            'Meta': {'object_name': 'Email'},
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_scheduled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'html_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '78'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'text_body': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mail']
