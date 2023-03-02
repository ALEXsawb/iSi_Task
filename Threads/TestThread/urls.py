from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import Thread, UserThreads, Messages, ReadMessages, all_unread_messages_by_thread, all_unread_messages

urlpatterns = [
    path(r'token-auth/', obtain_jwt_token),
    path(r'token-refresh/', refresh_jwt_token),
    path('drf-auth/', include('rest_framework.urls')),
    path(r'thread', Thread.as_view(), name='tread'),
    path(r'threads', UserThreads.as_view(), name='thread-list'),
    path(r'thread/<int:thread_id>', Messages.as_view(), name='message-list'),
    path(r'thread/<int:thread_id>/unread-messages', all_unread_messages_by_thread, name='unread-messages-by-thread'),
    path(r'read-messages', ReadMessages.as_view(), name='read-message'),
    path(r'unread-messages', all_unread_messages, name='unread-message')
]