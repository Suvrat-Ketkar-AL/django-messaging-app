from rest_framework import serializers
from .models import Message_Model, Reported_Message_Model
from drf_spectacular.utils import extend_schema_field
# Base fields common to both
class BaseMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    is_mod_message = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_mod_message(self, obj):
        return getattr(obj.sender, 'is_staff', False)

    class Meta:
        model = Message_Model
        fields = ['id', 'sender_username', 'content', 'timestamp', 'is_mod_message']
        read_only_fields = ['id', 'sender_username', 'timestamp', 'is_mod_message']

class UserMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        # Inherits all fields from Base except 'reported_by' and 'is_reported'
        pass

class AdminMessageSerializer(BaseMessageSerializer):
    reported_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_reported = serializers.BooleanField(read_only=True)

    class Meta(BaseMessageSerializer.Meta):
        fields = BaseMessageSerializer.Meta.fields + ['is_reported', 'reported_by']


class ReportedMessageSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source='reporter.username', read_only=True)
    message_id = serializers.IntegerField(source='message.id', read_only=True)
    message_content = serializers.CharField(source='message.content', read_only=True)

    class Meta:
        model = Reported_Message_Model
        fields = ['id', 'reporter', 'message_id', 'message_content', 'reason', 'reported_at']

