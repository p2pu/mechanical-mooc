# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'UserSignup', fields ['email']
        db.delete_unique('signup_usersignup', ['email'])

        # Rename field 'UserSignup.date_welcome_email_sent'
        db.rename_column('signup_usersignup', 'date_welcome_email_sent', 'date_tasks_handled')

        # Adding field 'UserSignup.date_deleted'
        db.add_column('signup_usersignup', 'date_deleted',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Changing field 'UserSignup.sequence'
        db.alter_column('signup_usersignup', 'sequence', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Rename field 'UserSignup.date_tasks_handled'
        db.rename_column('signup_usersignup', 'date_tasks_handled', 'date_welcome_email_sent')

        # Deleting field 'UserSignup.date_deleted'
        db.delete_column('signup_usersignup', 'date_deleted')

        # User chose to not deal with backwards NULL issues for 'UserSignup.sequence'
        raise RuntimeError("Cannot reverse this migration. 'UserSignup.sequence' and its values cannot be restored.")
        # Adding unique constraint on 'UserSignup', fields ['email']
        db.create_unique('signup_usersignup', ['email'])


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
