# Generated by Django 2.2.1 on 2019-06-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptime', '0003_auto_20190606_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptime',
            name='lap_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
