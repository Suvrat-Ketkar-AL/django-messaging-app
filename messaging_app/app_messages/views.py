from rest_framework import viewsets, permissions
from .models import Message_Model
from .serializers import MessageSerializer
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

class MessageViewSet(viewsets.ModelViewSet):
    # Specify the serializer class that will be used for validation and serialization
    serializer_class = MessageSerializer
    
    # Define the permission classes to enforce authentication
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Returns a queryset of all messages, ordered in reverse chronological order
        by the 'timestamp' field. This is used for actions like GET requests to
        list messages.
        """
        # The query returns all messages, ordered by the most recent first.
        return Message_Model.objects.all().order_by('-timestamp')
    
    def perform_create(self, serializer):
        """
        When a new message is being created, this method is called to set the
        'sender' field to the currently authenticated user.
        
        DRF automatically provides the logged-in user in the request object,
        which is accessible via `self.request.user`.
        """
        # Save the message with the currently authenticated user as the sender
        serializer.save(sender=self.request.user)
    
    def perform_update(self, serializer):
        """
        This method is invoked when a PUT or PATCH request is made to update
        an existing message. 
        
        - First, it retrieves the message that is being updated using `self.get_object()`.
        - Then, it checks if the sender of the message matches the current authenticated user.
        - If the message was created more than 5 minutes ago, it denies the update request.
        """
        # Retrieve the specific message object being updated from the database
        # `self.get_object()` will fetch the message based on the `pk` (primary key) in the URL
        message = self.get_object()

        # Check if the current user is the sender of the message
        # If not, raise a PermissionDenied exception
        if message.sender != self.request.user:
            raise PermissionDenied("You can only edit your own messages.")
        
        # Save the updated message (after any validation done in the serializer)
        serializer.save()
        
        # Check if the message was created within the last 5 minutes
        # If it's older, deny the update request
        if timezone.now() - message.timestamp > timedelta(minutes=5):
            raise PermissionDenied("You can only edit messages within 5 minutes of posting.")
    
    def perform_destroy(self, instance):
        """
        This method is used when a DELETE request is made to delete a message.
        
        - First, it checks if the user requesting the delete is the sender of the message.
        - If the sender is not the authenticated user, it raises a PermissionDenied exception.
        """
        # If the instance is not the logged-in user's message, deny the delete request
        if instance.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own messages unless you are an admin.")
        
        # Proceed to delete the message instance from the database
        instance.delete()
