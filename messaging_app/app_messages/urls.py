from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet,AdminMessageViewSet

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='messages')
router.register(r'admin/messages', AdminMessageViewSet, basename='admin-messages')

urlpatterns = [
    path('', include(router.urls)),
]
