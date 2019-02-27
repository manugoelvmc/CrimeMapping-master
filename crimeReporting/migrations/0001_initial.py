# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-27 20:13
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CRIME_TIMELINE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CURRENT_STATUS', models.CharField(choices=[('lodged', 'LODGED'), ('pending', 'PENDING'), ('investigated', 'INVESTIGATED'), ('evidence_collection', 'EVIDENCE COLLECTION'), ('moved', 'MOVED TO COURT'), ('closed', 'CLOSED')], default='Pending', max_length=100)),
                ('TIME_OF_UPDATE', models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 27, 20, 13, 56, 652500, tzinfo=utc))),
                ('DESCRIPTION', models.CharField(blank=True, default='Pending', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FIR_REPORT',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('CRIME_TYPE', models.CharField(max_length=100)),
                ('LAT', models.FloatField()),
                ('LNG', models.FloatField()),
                ('DATE_CRIME', models.DateField()),
                ('TIME_CRIME', models.TimeField()),
                ('COMPLAINT_TIME', models.TimeField(default=datetime.datetime(2019, 2, 27, 20, 13, 56, 651206, tzinfo=utc))),
                ('COMPLAINT_DATE', models.DateField(default=datetime.datetime(2019, 2, 27, 20, 13, 56, 651252, tzinfo=utc))),
                ('PHONE', models.CharField(max_length=100, null=True)),
                ('STATUS', models.CharField(choices=[('lodged', 'LODGED'), ('pending', 'PENDING'), ('investigated', 'INVESTIGATED'), ('evidence_collection', 'EVIDENCE COLLECTION'), ('moved', 'MOVED TO COURT'), ('closed', 'CLOSED')], default='Lodged', max_length=100)),
                ('CRIME_DESCRIPTION', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='INFORMATION_FILING_APP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crimetype', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.CharField(max_length=100)),
                ('crime_description', models.CharField(max_length=100)),
                ('date_crime', models.DateField()),
                ('time_crime', models.TimeField()),
                ('complaint_time', models.TimeField()),
                ('complaint_date', models.DateField()),
                ('isVerify', models.CharField(default='1', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='POLICE_STATION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('POLICE_STATION_LAT', models.FloatField()),
                ('POLICE_STATION_LNG', models.FloatField()),
                ('POLICE_ADDRESS', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='USER',
            fields=[
                ('USER_REF', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='USER', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('NAME', models.CharField(max_length=100)),
                ('LAT', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LAT', to='crimeReporting.POLICE_STATION')),
                ('LNG', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LNG', to='crimeReporting.POLICE_STATION')),
            ],
        ),
        migrations.AddField(
            model_name='information_filing_app',
            name='police_name',
            field=models.ForeignKey(db_column='NAME', on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.USER'),
        ),
        migrations.AddField(
            model_name='fir_report',
            name='FIR_LOC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.POLICE_STATION'),
        ),
        migrations.AddField(
            model_name='fir_report',
            name='PERSON_COMPLAINT',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.USER'),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='crime_timeline',
            name='CRIME_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.FIR_REPORT'),
        ),
        migrations.AddField(
            model_name='crime_timeline',
            name='UPDATED_BY',
            field=models.ForeignKey(db_column='NAME', on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.USER'),
        ),
    ]