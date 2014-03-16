# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Conference.no_refunds_start_date'
        db.alter_column(u'regimun_app_conference', 'no_refunds_start_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Conference.no_refunds_start_date'
        raise RuntimeError("Cannot reverse this migration. 'Conference.no_refunds_start_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Conference.no_refunds_start_date'
        db.alter_column(u'regimun_app_conference', 'no_refunds_start_date', self.gf('django.db.models.fields.DateField')())

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'regimun_app.committee': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'conference'), ('url_name', 'conference'))", 'object_name': 'Committee'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Conference']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        u'regimun_app.conference': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Conference'},
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'no_refunds_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'regimun_app.country': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'conference'), ('url_name', 'conference'))", 'object_name': 'Country'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Conference']"}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        u'regimun_app.countrypreference': {
            'Meta': {'ordering': "('last_modified',)", 'object_name': 'CountryPreference'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.DelegationRequest']"})
        },
        u'regimun_app.datepenalty': {
            'Meta': {'ordering': "('name',)", 'object_name': 'DatePenalty'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'based_on': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'feestructure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.FeeStructure']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'per': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'regimun_app.delegate': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Delegate'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position_assignment': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['regimun_app.DelegatePosition']", 'unique': 'True'})
        },
        u'regimun_app.delegatecountpreference': {
            'Meta': {'ordering': "('last_modified',)", 'object_name': 'DelegateCountPreference'},
            'delegate_count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['regimun_app.DelegationRequest']", 'unique': 'True'})
        },
        u'regimun_app.delegateposition': {
            'Meta': {'ordering': "('school', 'country', 'committee', 'title')", 'object_name': 'DelegatePosition'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Committee']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.School']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Delegate'", 'max_length': '200'})
        },
        u'regimun_app.delegationrequest': {
            'Meta': {'object_name': 'DelegationRequest'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Conference']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.School']"})
        },
        u'regimun_app.facultysponsor': {
            'Meta': {'ordering': "('user', 'phone')", 'object_name': 'FacultySponsor'},
            'conferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['regimun_app.Conference']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'faculty_sponsor'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'regimun_app.fee': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Fee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'feestructure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.FeeStructure']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'per': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'regimun_app.feestructure': {
            'Meta': {'object_name': 'FeeStructure'},
            'conference': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['regimun_app.Conference']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'regimun_app.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.Conference']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regimun_app.School']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'regimun_app.school': {
            'Meta': {'ordering': "('name',)", 'object_name': 'School'},
            'access_code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'conferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['regimun_app.Conference']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'regimun_app.secretariat': {
            'Meta': {'ordering': "('user',)", 'object_name': 'Secretariat'},
            'conferences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['regimun_app.Conference']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'secretariat_member'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['regimun_app']