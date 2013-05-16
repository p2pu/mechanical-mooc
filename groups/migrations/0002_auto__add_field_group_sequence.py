# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.sequence'
        db.add_column('groups_group', 'sequence',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Group.sequence'
        db.delete_column('groups_group', 'sequence')


    models = {
        'groups.group': {
            'Meta': {'object_name': 'Group'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'groups.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']