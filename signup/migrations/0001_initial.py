# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSignup'
        db.create_table('signup_usersignup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('invite_code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('questions', self.gf('django.db.models.fields.TextField')()),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_deleted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_tasks_handled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('signup', ['UserSignup'])


    def backwards(self, orm):
        # Deleting model 'UserSignup'
        db.delete_table('signup_usersignup')


    models = {
        'signup.usersignup': {
            'Meta': {'object_name': 'UserSignup'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'date_deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_tasks_handled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'questions': ('django.db.models.fields.TextField', [], {}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['signup']