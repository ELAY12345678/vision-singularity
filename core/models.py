from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class Table(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    number     = models.PositiveIntegerField()
    camera_id  = models.CharField(max_length=50)  # which camera sees it

    class Meta:
        unique_together = ('restaurant', 'number')

    def __str__(self):
        return f"{self.restaurant.name} – Table {self.number}"

class ServiceCall(models.Model):
    EVENT_CHOICES = (
        ('hand_raise', 'Hand Raise'),
        ('wave',       'Wave'),
    )
    table      = models.ForeignKey(Table, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=20, default='pending')  # pending/handled

    class Meta:
        ordering = ['-created_at']  # Clearly added ordering here (newest first)

    def __str__(self):
        return f"{self.table} – {self.event_type} @ {self.created_at:%H:%M:%S}"
    
@receiver(post_save, sender=ServiceCall)
def send_service_call_event(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "waiters_group",
            {
                "type": "send_service_call",
                "content": {
                    "id": instance.id,
                    "table": instance.table.number,
                    "event_type": instance.event_type,
                    "status": instance.status,
                    "created_at": str(instance.created_at),
                }
            }
        )
