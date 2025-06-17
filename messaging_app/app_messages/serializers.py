from rest_framework import serializers
from .models import Message_Model, Reported_Message_Model
from drf_spectacular.utils import extend_schema_field

# fields common to both
class UserMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')
    is_mod_message = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_mod_message(self, obj):
        return getattr(obj.sender, 'is_staff', False)

    class Meta:
        model = Message_Model
        fields = ['id', 'sender_username', 'content', 'timestamp', 'is_mod_message']
        read_only_fields = ['id', 'sender_username', 'timestamp', 'is_mod_message']


class AdminMessageSerializer(UserMessageSerializer):
    reported_by = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    is_reported = serializers.BooleanField()

    class Meta(UserMessageSerializer.Meta):
        fields = UserMessageSerializer.Meta.fields + ['is_reported', 'reported_by']
        read_only_fields = UserMessageSerializer.Meta.read_only_fields + ['is_reported', 'reported_by']


class ReportedMessageSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source='reporter.username')
    message_id = serializers.IntegerField(source='message.id')
    message_content = serializers.CharField(source='message.content')

    class Meta:
        model = Reported_Message_Model
        fields = ['id', 'reporter', 'message_id', 'message_content', 'reason', 'reported_at']
        read_only_fields = ['id', 'reporter', 'message_id', 'message_content', 'reported_at']
