# Generated by Django 4.0 on 2022-07-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carshowroom', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carshowroommodel',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
