from rest_framework import serializers
from .models import Event, EventParticipant
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'current_participants', 'created_at', 'updated_at']

    def validate(self, data):
        if data['start_date'] < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past.")

        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be before end date.")

        if data['min_participants'] > data['max_participants']:
            raise serializers.ValidationError("Minimum participants can't exceed maximum.")
        return data

class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['organizer','title','location_name','current_participants','start_date']


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ['user','event','joined_at']





