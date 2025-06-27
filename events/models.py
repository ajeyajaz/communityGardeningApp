from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    organizer = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location_name = models.TextField()


    # Date and Time
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Capacity
    max_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        default=100
    )
    min_participants = models.PositiveIntegerField(default=1)
    current_participants = models.PositiveIntegerField(default=0)

    #status
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='upcoming')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['location_name']),
            models.Index(fields=['organizer']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title}"


class EventParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # prevent duplicate

    def __str__(self):
        return f"{self.user.username} joined {self.event.title}"




