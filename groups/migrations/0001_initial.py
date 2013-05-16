# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('groups_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('groups', ['Group'])

        # Adding model 'GroupMember'
        db.create_table('groups_groupmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='members', to=orm['groups.Group'])),
        ))
        db.send_create_signal('groups', ['GroupMember'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('groups_group')

        # Deleting model 'GroupMember'
        db.delete_table('groups_groupmember')


    models = {
        'groups.group': {
            'Meta': {'object_name': 'Group'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'groups.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']