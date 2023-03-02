from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .paginations import MessagePagination, ThreadPagination
from .permissions import IsParticipantOfThread
from .serializers import *
from .services import model_utilities


class Thread(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = ThreadCreateSerializer

    def create(self, request, *args, **kwargs):
        thread = model_utilities.get_thread_instance_if_thread_with_specified_users_exist([request.data['participant'],
                                                                                           self.request.user.id])
        if thread:
            response_data = ThreadDetailSerializes(thread, context={'user': self.request.user})
            return Response(response_data.data, status=status.HTTP_200_OK,
                            headers=self.get_success_headers(response_data.data))
        else:
            return super().create(request, *args, **kwargs)


class UserThreads(generics.ListAPIView):
    serializer_class = UserThreadsSerializer
    pagination_class = ThreadPagination

    def get_queryset(self):
        return model_utilities.get_user_threads(user_id=self.request.user.id)

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


class Messages(generics.ListCreateAPIView, ):
    serializer_class = MessagesSerializer
    permission_classes = [IsParticipantOfThread, IsAuthenticated]
    pagination_class = MessagePagination
    lookup_field = 'thread_id'

    def get_queryset(self):
        return model_utilities.get_messages(self.request.user.pk, self.kwargs['thread_id'])

    def create(self, request, *args, **kwargs):
        request.data['sender'] = model_to_dict(request.user)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.data
        model_utilities.create_message(sender_id=data['sender']['id'],
                                       thread_id=self.request.parser_context['kwargs']['thread_id'],
                                       text=data['text'])


class ReadMessages(generics.UpdateAPIView):
    serializer_class = ReadMessageSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = [{'id': message_id} for message_id in kwargs['data']['message_ids']]
        return super(ReadMessages, self).get_serializer(many=True if len(args[0]) > 1 else False,
                                                        *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = model_utilities.get_dont_belong_user_unread_messages_by_id(self.request.data['message_ids'],
                                                                         self.request.user.pk)
        if obj:
            return obj
        raise NotFound(detail='Unread message by specified id don`t exist.')


@api_view()
def all_unread_messages_by_thread(request, thread_id):
    response_data = {'unread_messages':
                         {'count': model_utilities.get_all_unread_messages_by_specified_thread(user_id=request.user.id,
                                                                                               thread_id=thread_id)}}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view()
def all_unread_messages(request):
    response_data = {'unread_messages': {'count': model_utilities.get_all_unread_messages(user_id=request.user.id)}}
    return Response(response_data, status=status.HTTP_200_OK)
