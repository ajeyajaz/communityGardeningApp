from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from comments.models import Comment
from notifications.utils import create_notification
from events.models import Event, EventParticipant


# only organizer will get notifications
@receiver(post_save, sender=Comment)
def notify_event_organizer_on_comment(sender, instance, created, **kwargs):
    if created and instance.event.organizer != instance.user:
        message = f"{instance.user.username} commented on your event '{instance.event.title}'."
        create_notification(instance.event.organizer, message)


# all participants well get notifications
@receiver(post_save, sender=Event)
def notify_event_update(sender, instance, created, **kwargs):
    if created:
        return  # Only trigger on update, not creation

    # Get all participants except the organizer
    participants = EventParticipant.objects.filter(event=instance).exclude(user=instance.organizer)

    for participant in participants:
        create_notification(
            user=participant.user,
            message=f"The event '{instance.title}' has been updated."
        )

# only organizer will get notifications
@receiver(post_save, sender=EventParticipant)
def notify_join(sender, instance, created, **kwargs):
    if created:
        create_notification(
            user=instance.event.organizer,
            message=f"{instance.user.username} joined your event '{instance.event.title}'."
        )

# only organizer will get notifications
@receiver(post_delete, sender=EventParticipant)
def notify_leave(sender, instance, **kwargs):
    create_notification(
        user=instance.event.organizer,
        message=f"{instance.user.username} left your event '{instance.event.title}'."
    )

