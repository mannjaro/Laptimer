from django.db import models
from django.utils.duration import duration_string


class Car(models.Model):
    car_no = models.IntegerField()
    car_name = models.CharField(max_length=64)
    team_name = models.CharField(max_length=128)
    univ_name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.car_no)


class SensorInput(models.Model):
    module = models.CharField(max_length=32)
    input_data = models.IntegerField(blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, related_name='source_car', blank=True, null=True)

    def __str__(self):
        return str(self.input_data)

    def __sub__(self, other):
        return self.input_data - other.input_data


class LapTime(models.Model):
    STATUS = (
        ('IN', 'IN_LAP'),
        ('STAY', 'STAY_OUT'),
        ('OUT', 'OUT_LAP'),
    )
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, related_name='car', blank=True, null=True)
    start_time = models.ForeignKey(SensorInput, on_delete=models.DO_NOTHING, related_name='start_time')
    end_time = models.ForeignKey(SensorInput, on_delete=models.DO_NOTHING, related_name='end_time', blank=True, null=True)
    lap_time = models.BigIntegerField(blank=True, null=True)
    lap_status = models.CharField(max_length=4, choices=STATUS)

    def __str__(self):
        return str(self.lap_time)
