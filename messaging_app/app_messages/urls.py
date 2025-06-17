from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserMessageViewSet, AdminMessageViewSet

router = DefaultRouter()
router.register(r'user/messages', UserMessageViewSet, basename='user-messages')
router.register(r'admin/messages', AdminMessageViewSet, basename='admin-messages')

urlpatterns = [
    path('', include(router.urls)),
]
