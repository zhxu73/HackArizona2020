# Generated by Django 3.0.2 on 2020-01-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_auto_20200119_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='departure_date',
            new_name='departure_time',
        ),
        migrations.AddField(
            model_name='userdata',
            name='airport',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='city',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='flight_json',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='flight_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
