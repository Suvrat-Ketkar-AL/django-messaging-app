from rest_framework import serializers
from .models import Message_Model

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message_Model
        fields = ['id','sender_username', 'content', 'timestamp', 'is_reported', 'reported_by']
        extra_kwargs = {
            'content': {'required': True, 'allow_blank': False},  # Ensure content is required and not blank
            'is_reported': {'required': False},  # Allow is_reported to be optional
            'reported_by': {'required': False}  # Allow reported_by to be optional
        }
        read_only_fields = ['id','sender_username', 'timestamp'] #ignore these fields during creation and update
