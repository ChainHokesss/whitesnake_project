# Generated by Django 4.0 on 2022-07-13 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodel',
            name='car_charact',
            field=models.JSONField(default=''),
        ),
    ]