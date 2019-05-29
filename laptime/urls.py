from rest_framework import routers
from laptime.views import CarViewSets, SensorViewSets, LapTimeViewSets


router = routers.DefaultRouter()
router.register('car', CarViewSets)
router.register('sensor', SensorViewSets)
router.register('laptime', LapTimeViewSets)
