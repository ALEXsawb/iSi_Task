from collections import OrderedDict

from django.forms import model_to_dict
from rest_framework import serializers

from .services.model_utilities import get_last_message_of_thread
from .models import ThreadModel, MessageModel
from django.contrib.auth.models import User


class ThreadCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participant = serializers.IntegerField(min_value=1, source='participant2.id')

    def create(self, validated_data):
        new_thread = ThreadModel(participant1_id=validated_data['user'].id,
                                 participant2_id=validated_data['participant2']['id'])
        new_thread.save()
        return new_thread

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['participant'] = UserSerializer(User.objects.get(pk=result['participant'])).data
        return result

    class Meta:
        model = ThreadModel
        fields = ['id', 'participant', 'user']


class ThreadDetailSerializes(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField()

    def get_participant(self, instance):
        participant = instance.participant2 if instance.participant2 != self.context['user'] else instance.participant1
        return UserSerializer(participant, context=self.context).data

    class Meta:
        model = ThreadModel
        fields = ['id', 'participant']


class UserThreadsSerializer(ThreadDetailSerializes):
    last_message = serializers.SerializerMethodField(allow_null=True)

    def get_last_message(self, instance):
        last_message = get_last_message_of_thread(instance)
        if last_message:
            return MessagesSerializer(last_message, context=self.context).data
        else:
            return None

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = ThreadModel
        fields = ['id', 'participant', 'last_message']


class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    def get_sender(self, instance):
        if not hasattr(instance, 'sender'):
            return UserSerializer({'username': self._kwargs['data']['sender']['username'], 'id': self._kwargs['data']['sender']['id']},
                                  context=self.context).data
        return UserSerializer({'username': instance.sender.username, 'id': instance.sender.id},
                              context=self.context).data

    class Meta:
        model = MessageModel
        fields = ['id', 'sender', 'text', 'created', 'is_read']
        extra_kwargs = {'is_read': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {'username': {'read_only': True}}


class ReadMessagesSerializer(serializers.ListSerializer):
    def update(self, messages, validated_data):
        return [self.child.update(message) for message in messages]


class ReadMessageSerializer(serializers.ModelSerializer):

    def update(self, instance):
        instance.is_read = True
        instance.save()
        return instance

    class Meta:
        model = MessageModel
        list_serializer_class = ReadMessagesSerializer
        fields = ['id', 'is_read']
