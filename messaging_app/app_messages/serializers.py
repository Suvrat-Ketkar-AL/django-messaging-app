from rest_framework import serializers
from .models import Message_Model

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message_Model
        fields = ['id','sender_username', 'content', 'timestamp']
        read_only_fields = ['id','sender_username', 'timestamp'] #ignore these fields during creation and update
