from rest_framework import serializers
from .models import Event, EventParticipant
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'current_participants', 'created_at', 'updated_at']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        min_p = data.get('min_participants')
        max_p = data.get('max_participants')

        if start_date  < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past.")

        if start_date >= end_date:
            raise serializers.ValidationError("Start date must be before end date.")

        if min_p > max_p:
            raise serializers.ValidationError("Minimum participants can't exceed maximum.")
        return data




class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['organizer','title','location_name','current_participants','start_date']


class EventEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['title', 'description', 'location_name', 'start_date',
                  'end_date','min_participants', 'max_participants']

        def validate(self, data):
            start_date = data.get('start_date', self.instance.start_date)
            end_date = data.get('end_date', self.instance.end_date)

            if start_date and end_date and end_date <= start_date:
                raise serializers.ValidationError("End date must be after start date.")

            if start_date and start_date < timezone.now():
                raise serializers.ValidationError("Start date cannot be in the past.")

            return data


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ['user','event','joined_at']







