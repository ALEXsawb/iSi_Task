from rest_framework import permissions

from .services.model_utilities import check_specified_participant_is_of_the_specified_thread_or_not


class IsParticipantOfThread(permissions.BasePermission):
    def has_permission(self, request, view):
        if check_specified_participant_is_of_the_specified_thread_or_not(request.user.id,
                                                                         request.parser_context['kwargs']['thread_id']):
            return True
        return False
