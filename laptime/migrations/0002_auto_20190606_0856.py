# Generated by Django 2.2.1 on 2019-06-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptime',
            name='lap_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]