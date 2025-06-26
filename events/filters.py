import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name='start_date')
    location = django_filters.CharFilter(field_name='location_name', lookup_expr='icontains')
    organizer = django_filters.NumberFilter(field_name='organizer_id')

    class Meta:
        model = Event
        fields = ['date', 'location_name', 'organizer']
