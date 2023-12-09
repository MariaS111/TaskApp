from rest_framework.permissions import BasePermission
from tasks.models import TeamBoard


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCreator(BasePermission):

    def has_permission(self, request, view):
        obj = view.get_object()
        return obj.user == request.user


class IsInWatchersOrCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.watchers.all() or obj.user == request.user


class IsInParticipantsInAdminsOrCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.participants.all() or request.user in obj.admins.all() or obj.user == request.user


class IsInAdminsOrCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.admins.all() or obj.user == request.user


class IsCreatorOrInParticipantsOrInAdminsForTask(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        user = request.user
        team_board = obj.team_board
        return user == team_board.user or user in team_board.participants.all() or user in team_board.admins.all()


class IsCreatorOrInAdminsForTask(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        user = request.user
        team_board = obj.team_board
        return user == team_board.user or user in team_board.admins.all()


class IsCreatorOrInAdminsForCreatingTask(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        team_board = TeamBoard.objects.get(pk=view.kwargs['teamboard_pk'])
        return user == team_board.user or user in team_board.admins.all()


class CanViewComments(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        team_board = TeamBoard.objects.get(pk=view.kwargs['teamboard_pk'])
        return user == team_board.user or user in team_board.admins.all() or user in team_board.participants.all()