# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conference'
        db.create_table(u'regimun_app_conference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('address_country', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('no_refunds_start_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'regimun_app', ['Conference'])

        # Adding model 'FeeStructure'
        db.create_table(u'regimun_app_feestructure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['regimun_app.Conference'], unique=True)),
        ))
        db.send_create_signal(u'regimun_app', ['FeeStructure'])

        # Adding model 'Fee'
        db.create_table(u'regimun_app_fee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feestructure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.FeeStructure'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
            ('per', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'regimun_app', ['Fee'])

        # Adding model 'DatePenalty'
        db.create_table(u'regimun_app_datepenalty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feestructure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.FeeStructure'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
            ('per', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('based_on', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'regimun_app', ['DatePenalty'])

        # Adding model 'Committee'
        db.create_table(u'regimun_app_committee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Conference'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(max_length=200)),
        ))
        db.send_create_signal(u'regimun_app', ['Committee'])

        # Adding unique constraint on 'Committee', fields ['name', 'conference']
        db.create_unique(u'regimun_app_committee', ['name', 'conference_id'])

        # Adding unique constraint on 'Committee', fields ['url_name', 'conference']
        db.create_unique(u'regimun_app_committee', ['url_name', 'conference_id'])

        # Adding model 'Country'
        db.create_table(u'regimun_app_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Conference'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['Country'])

        # Adding unique constraint on 'Country', fields ['name', 'conference']
        db.create_unique(u'regimun_app_country', ['name', 'conference_id'])

        # Adding unique constraint on 'Country', fields ['url_name', 'conference']
        db.create_unique(u'regimun_app_country', ['url_name', 'conference_id'])

        # Adding model 'School'
        db.create_table(u'regimun_app_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('address_country', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('access_code', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'regimun_app', ['School'])

        # Adding M2M table for field conferences on 'School'
        m2m_table_name = db.shorten_name(u'regimun_app_school_conferences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm[u'regimun_app.school'], null=False)),
            ('conference', models.ForeignKey(orm[u'regimun_app.conference'], null=False))
        ))
        db.create_unique(m2m_table_name, ['school_id', 'conference_id'])

        # Adding model 'DelegatePosition'
        db.create_table(u'regimun_app_delegateposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Country'])),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Committee'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.School'], null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Delegate', max_length=200)),
        ))
        db.send_create_signal(u'regimun_app', ['DelegatePosition'])

        # Adding model 'Delegate'
        db.create_table(u'regimun_app_delegate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position_assignment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['regimun_app.DelegatePosition'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['Delegate'])

        # Adding model 'FacultySponsor'
        db.create_table(u'regimun_app_facultysponsor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='faculty_sponsor', unique=True, to=orm['auth.User'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.School'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['FacultySponsor'])

        # Adding M2M table for field conferences on 'FacultySponsor'
        m2m_table_name = db.shorten_name(u'regimun_app_facultysponsor_conferences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facultysponsor', models.ForeignKey(orm[u'regimun_app.facultysponsor'], null=False)),
            ('conference', models.ForeignKey(orm[u'regimun_app.conference'], null=False))
        ))
        db.create_unique(m2m_table_name, ['facultysponsor_id', 'conference_id'])

        # Adding model 'Secretariat'
        db.create_table(u'regimun_app_secretariat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='secretariat_member', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'regimun_app', ['Secretariat'])

        # Adding M2M table for field conferences on 'Secretariat'
        m2m_table_name = db.shorten_name(u'regimun_app_secretariat_conferences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('secretariat', models.ForeignKey(orm[u'regimun_app.secretariat'], null=False)),
            ('conference', models.ForeignKey(orm[u'regimun_app.conference'], null=False))
        ))
        db.create_unique(m2m_table_name, ['secretariat_id', 'conference_id'])

        # Adding model 'DelegationRequest'
        db.create_table(u'regimun_app_delegationrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.School'])),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Conference'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['DelegationRequest'])

        # Adding model 'CountryPreference'
        db.create_table(u'regimun_app_countrypreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.DelegationRequest'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Country'])),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'regimun_app', ['CountryPreference'])

        # Adding model 'DelegateCountPreference'
        db.create_table(u'regimun_app_delegatecountpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['regimun_app.DelegationRequest'], unique=True)),
            ('delegate_count', self.gf('django.db.models.fields.IntegerField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['DelegateCountPreference'])

        # Adding model 'Payment'
        db.create_table(u'regimun_app_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.School'])),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regimun_app.Conference'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
        ))
        db.send_create_signal(u'regimun_app', ['Payment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Country', fields ['url_name', 'conference']
        db.delete_unique(u'regimun_app_country', ['url_name', 'conference_id'])

        # Removing unique constraint on 'Country', fields ['name', 'conference']
        db.delete_unique(u'regimun_app_country', ['name', 'conference_id'])

        # Removing unique constraint on 'Committee', fields ['url_name', 'conference']
        db.delete_unique(u'regimun_app_committee', ['url_name', 'conference_id'])

        # Removing unique constraint on 'Committee', fields ['name', 'conference']
        db.delete_unique(u'regimun_app_committee', ['name', 'conference_id'])

        # Deleting model 'Conference'
        db.delete_table(u'regimun_app_conference')

        # Deleting model 'FeeStructure'
        db.delete_table(u'regimun_app_feestructure')

        # Deleting model 'Fee'
        db.delete_table(u'regimun_app_fee')

        # Deleting model 'DatePenalty'
        db.delete_table(u'regimun_app_datepenalty')

        # Deleting model 'Committee'
        db.delete_table(u'regimun_app_committee')

        # Deleting model 'Country'
        db.delete_table(u'regimun_app_country')

        # Deleting model 'School'
        db.delete_table(u'regimun_app_school')

        # Removing M2M table for field conferences on 'School'
        db.delete_table(db.shorten_name(u'regimun_app_school_conferences'))

        # Deleting model 'DelegatePosition'
        db.delete_table(u'regimun_app_delegateposition')

        # Deleting model 'Delegate'
        db.delete_table(u'regimun_app_delegate')

        # Deleting model 'FacultySponsor'
        db.delete_table(u'regimun_app_facultysponsor')

        # Removing M2M table for field conferences on 'FacultySponsor'
        db.delete_table(db.shorten_name(u'regimun_app_facultysponsor_conferences'))

        # Deleting model 'Secretariat'
        db.delete_table(u'regimun_app_secretariat')

        # Removing M2M table for field conferences on 'Secretariat'
        db.delete_table(db.shorten_name(u'regimun_app_secretariat_conferences'))

        # Deleting model 'DelegationRequest'
        db.delete_table(u'regimun_app_delegationrequest')

        # Deleting model 'CountryPreference'
        db.delete_table(u'regimun_app_countrypreference')

        # Deleting model 'DelegateCountPreference'
        db.delete_table(u'regimun_app_delegatecountpreference')

        # Deleting model 'Payment'
        db.delete_table(u'regimun_app_payment')


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
            'no_refunds_start_date': ('django.db.models.fields.DateField', [], {}),
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