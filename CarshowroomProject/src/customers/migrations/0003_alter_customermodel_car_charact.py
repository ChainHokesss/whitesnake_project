# Generated by Django 4.0 on 2022-07-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customermodel_car_charact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermodel',
            name='car_charact',
            field=models.JSONField(default={}),
        ),
    ]
