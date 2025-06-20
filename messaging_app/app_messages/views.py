from .models import Message_Model, Reported_Message_Model
from django.contrib.auth.models import User
from .serializers import UserMessageSerializer, AdminMessageSerializer, ReportedMessageSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

from django.shortcuts import get_object_or_404

class BaseMessageViewSet(viewsets.ModelViewSet):
    queryset = Message_Model.objects.all().order_by('-timestamp')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['content']
    permission_classes = [permissions.IsAuthenticated]

# Regular user ViewSet
class UserMessageViewSet(BaseMessageViewSet):
    
    serializer_class = UserMessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        message = self.get_object()
        if message.sender != self.request.user:
            raise PermissionDenied("You can only edit your own messages.")
        if timezone.now() - message.timestamp > timedelta(minutes=5):
            raise PermissionDenied("You can only edit messages within 5 minutes of posting.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own messages unless you are an admin.")
        instance.delete()
    
    @action(detail=True, methods=['post'],url_path='report-message')
    def report(self, request, pk=None):
        """
        Allows a user to report a message. A user can report a message only once.
        """
        message = self.get_object()
        user = request.user
        reason = request.data.get('reason')
        if not reason:
            return Response({"detail": "Reason for reporting is required."}, status=400)

        if Reported_Message_Model.objects.filter(message=message, reporter=user).exists():
            return Response({"detail": "You have already reported this message."}, status=400)

        Reported_Message_Model.objects.create(message=message, reporter=user, reason=reason)
        message.is_reported = True
        message.save()


        return Response({"detail": "Message reported successfully."}, status=200)

    @action(detail=True, methods=['post'], url_path='bookmark')
    def add_bookmark(self, request, pk=None):
        user = request.user
        message = self.get_object()
        if user in message.bookmarked_by.all():
            return Response({"detail": "You have already bookmarked this message."}, status=400)
        message.bookmarked_by.add(user)
        return Response({"detail": "Message bookmarked successfully."}, status=200)
    
    @action(detail=False, methods=['get'], url_path='view-bookmarks')
    def view_bookmarks(self, request):
        """
        Allows a user to view their bookmarked messages.
        """
        user = request.user
        bookmarked_messages = Message_Model.objects.filter(bookmarked_by=user)
        serializer = self.get_serializer(bookmarked_messages, many=True)
        return Response(serializer.data)


# Admin-only ViewSet
class AdminMessageViewSet(UserMessageViewSet):
    
    serializer_class = AdminMessageSerializer
    permission_classes = [permissions.IsAdminUser]

    # Admin can delete any message
    def perform_destroy(self, instance):
        instance.delete()

    # Admin can view reported messages
    @action(detail=False, methods=['get'], url_path='reported-messages')
    def reported_messages(self, request):
        reported_msgs = Reported_Message_Model.objects.all().order_by('-reported_at')
        serializer = ReportedMessageSerializer(reported_msgs, many=True)
        return Response(serializer.data)

    # Admin can redact a message
    @action(detail=True, methods=['post'], url_path='redact')
    def redact_message(self, request, pk=None):
        message = self.get_object()
        message.content = "[Message redacted by admin]"
        message.save()
        return Response({'status': 'message redacted'})

    # Admin can suspend a user
    @action(detail=True, methods=['post'], url_path='suspend-user')
    def suspend_user(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response({'status': f'User {user.username} has been suspended'})
