# Generated by Django 5.2.3 on 2025-06-17 09:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_messages', '0005_remove_message_model_reported_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message_model',
            name='reported_by',
            field=models.ManyToManyField(blank=True, related_name='reported_messages', through='app_messages.Reported_Message_Model', to=settings.AUTH_USER_MODEL),
        ),
    ]
