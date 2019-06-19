from rest_framework import serializers
from laptime.models import Car, SensorInput, LapTime

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class LapTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LapTime
        fields = '__all__'


class ChannelSerializer(serializers.Serializer):
    channel = serializers.IntegerField(required=False, write_only=True)
    type = serializers.CharField(max_length=8,required=False, write_only=True)
    value = serializers.IntegerField(required=True)
    datetime = serializers.DateTimeField(required=False, write_only=True)


class PayloadSerializer(serializers.Serializer):
    channels = ChannelSerializer(many=True)


class SensorSerializer(serializers.ModelSerializer):
    module = serializers.CharField(max_length=32)
    type = serializers.CharField(max_length=32, required=False, write_only=True)
    datetime = serializers.DateTimeField(required=False, write_only=True)
    payload = PayloadSerializer(required=False, write_only=True)
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), required=False)
    in_lap = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = SensorInput
        fields = ('id','module', 'type', 'datetime', 'payload', 'in_lap', 'car', 'input_data')
        extra_kwargs = {
            'type': {'write_only': True},
            'datetime': {'write_only': True}
        }

    def create(self, validated_data):
        channel = validated_data['payload']['channels']
        for value in channel:
            if value['channel'] == 0:
                progress_time = value['value']
            elif value['channel'] == 1:
                startup_time = value['value']

        sensor_data = SensorInput(
            module=validated_data['module'],
            input_data=progress_time + startup_time,
        )
        sensor_data.save()
        return sensor_data

    def update(self, instance, validated_data):
        instance.car = validated_data.get('car', instance.car)
        instance.save()

        lap_time = {
            'start_time': instance,
            'car': instance.car,
            'lap_status': 'STAY',
        }
        """
        Status: 
        1. If in_lap flag is set, latest instance will be updated status and end_time.
        2. Else if this have end_lap data, this lap may be OUTLAP so that new instance will be created.
        3. When other status, this is measurement lap. And this.end_time is set and new instance will be created.
        Note: When first lap for this car (LapTime.DoesNotExist), instance will be created.
        """
        try:
            "Status: 1"
            lap = LapTime.objects.filter(car_id=instance.car).latest('start_time__input_data')
            if validated_data['in_lap']:
                lap.end_time = instance
                lap.lap_status = 'IN'
                lap.lap_time = lap.end_time - lap.start_time
                lap.save()

            else:
                if lap.end_time is not None:
                    "Status: 2"
                    lap_time['lap_status'] = 'OUT'
                    LapTime.objects.create(**lap_time)
                else:
                    "Status: 3"
                    lap.end_time = instance
                    lap.lap_time = lap.end_time - lap.start_time
                    lap.save()

                    LapTime.objects.create(**lap_time)
        except LapTime.DoesNotExist:
            lap_time['lap_status'] = 'OUT'
            LapTime.objects.create(**lap_time)

        return instance
