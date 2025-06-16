from rest_framework import serializers
from .models import Message_Model

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message_Model
        fields = ['id','sender_username', 'content', 'timestamp', 'is_reported', 'reported_by']
        extra_kwargs = {
            'content': {'required': True, 'allow_blank': False},  # Ensure content is required and not blank
        }
        read_only_fields = ['id','sender_username', 'timestamp'] #ignore these fields during creation and update
    
    def to_representation(self, instance):
        # Get the default representation
        rep = super().to_representation(instance)

        # Get the request context
        request = self.context.get('request')
        
        # Check if request and user are available, and if user is not staff
        if request and not request.user.is_staff:
            # Remove these fields for non-admin users
            rep.pop('is_reported', None)  # Remove 'is_reported' if exists
            rep.pop('reported_by', None)  # Remove 'reported_by' if exists
        
        return rep