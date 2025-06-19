from django.contrib import admin

# Register your models here.
from .models import Message_Model, Reported_Message_Model

@admin.register(Message_Model)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content', 'timestamp', 'is_reported')
    search_fields = ('sender__username', 'content')
    list_filter = ('is_reported', 'timestamp')

@admin.register(Reported_Message_Model)
class ReportedMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'reporter', 'reason', 'reported_at')
    search_fields = ('reporter__username', 'message__content')
    list_filter = ('reason', 'reported_at')
