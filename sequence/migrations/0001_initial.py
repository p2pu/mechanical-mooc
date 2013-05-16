# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sequence'
        db.create_table('sequence_sequence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup_close_date', self.gf('django.db.models.fields.DateField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('sequence', ['Sequence'])


    def backwards(self, orm):
        # Deleting model 'Sequence'
        db.delete_table('sequence_sequence')


    models = {
        'sequence.sequence': {
            'Meta': {'object_name': 'Sequence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signup_close_date': ('django.db.models.fields.DateField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['sequence']