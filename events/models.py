from django.db import models
from django.contrib.auth.models import User
import os
import uuid  # Import uuid for unique registration IDs

def event_banner_upload_path(instance, filename):
    """Stores event banners in static/images/event_banners/"""
    return os.path.join('static/images/event_banners/', filename)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to=event_banner_upload_path, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, default="Online")

    def __str__(self):
        return self.name

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    class Meta:
        unique_together = ('user', 'event')  # Ensures a user registers only once per event

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
