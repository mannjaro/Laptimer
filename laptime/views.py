from rest_framework import viewsets
from laptime.models import Car, SensorInput, LapTime
from laptime.serializer import CarSerializer, SensorSerializer, LapTimeSerializer
from django_filters import rest_framework as filters


class LapTimeFilters(filters.FilterSet):
    car = filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = LapTime
        fields = ['car']


class CarViewSets(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class SensorViewSets(viewsets.ModelViewSet):
    queryset = SensorInput.objects.all()
    serializer_class = SensorSerializer


class LapTimeViewSets(viewsets.ModelViewSet):
    queryset = LapTime.objects.filter(lap_time__isnull=False)
    serializer_class = LapTimeSerializer
    filter_class = LapTimeFilters
