from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    if instance.status in ['approved', 'rejected']:
        message = f'Your request to join the team {instance.team.name} has been {instance.status}.'
        Notification.objects.create(user=instance.applicant, message=message)
