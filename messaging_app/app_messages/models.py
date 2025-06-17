from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message_Model(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_messages', blank=True)
    
    is_reported = models.BooleanField(default=False)
    reported_by = models.ManyToManyField(User, through='Reported_Message_Model',related_name='reported_messages', blank=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    
class Reported_Message_Model(models.Model):
    Report_Reason_Choices = [
        ('spam', 'Spam'),
        ('abuse', 'Abuse'),
        ('other', 'Other'),
    ]
    message = models.ForeignKey(Message_Model, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=5, choices=Report_Reason_Choices)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'reporter')  # Prevent duplicate reports

    def __str__(self):
        return f"Report by {self.reported.username} for message {self.message.id} at {self.timestamp}"