from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message_Model(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)
    reported_by = models.ManyToManyField(User, related_name='reported_messages', blank=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_messages', blank=True)
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"