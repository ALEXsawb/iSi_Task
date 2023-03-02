from typing import List, Optional

from django.db.models import Q

from ..models import ThreadModel, MessageModel


def get_thread_instance_if_thread_with_specified_users_exist(participants_ids: List[int]) -> Optional[ThreadModel]:
    try:
        participant1, participant2 = participants_ids
        return ThreadModel.objects.get(Q(Q(Q(participant1=participant1) & Q(participant2=participant2)) |
                                         Q(Q(participant1=participant2) & Q(participant2=participant1))))
    except ThreadModel.DoesNotExist:
        return False


def check_specified_participant_is_of_the_specified_thread_or_not(user_id: int, thread_id: int) -> bool:
    return ThreadModel.objects.filter(Q(id=thread_id) & Q(Q(participant1=user_id) | Q(participant2=user_id))).exists()


def get_user_threads(user_id: int) -> Optional[ThreadModel]:
    return ThreadModel.objects.filter(Q(participant1=user_id) | Q(participant2=user_id))


def get_messages(user_id: int, thread_id: int) -> List[MessageModel]:
    return MessageModel.objects.select_related('sender').filter(Q(Q(thread__participant1=user_id) |
                                                                  Q(thread__participant2=user_id)
                                                                  & Q(thread__pk=thread_id)))


def get_all_unread_messages_by_specified_thread(user_id: int, thread_id: int) -> List[MessageModel]:
    return MessageModel.objects.filter(Q(Q(thread__participant1=user_id) | Q(thread__participant2=user_id) &
                                         Q(thread__pk=thread_id)) & Q(is_read=False) & ~Q(sender__id=user_id)).count()


def get_all_unread_messages(user_id: int) -> List[MessageModel]:
    return MessageModel.objects.filter(Q(Q(thread__participant1=user_id) | Q(thread__participant2=user_id)) &
                                       Q(is_read=False) & ~Q(sender__id=user_id)).count()


def get_last_message_of_thread(thread: ThreadModel) -> Optional[ThreadModel]:
    try:
        return MessageModel.objects.select_related('sender').filter(thread=thread).last()
    except MessageModel.DoesNotExist:
        return False


def get_dont_belong_user_unread_messages_by_id(ids: List[int], user_id):
    return MessageModel.objects.filter(Q(pk__in=ids) & ~Q(sender__pk=user_id) & Q(is_read=False))


def create_message(sender_id: int, thread_id: int, text: str):
    MessageModel.objects.create(sender_id=sender_id, thread_id=thread_id, text=text)
