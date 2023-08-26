from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return obj.user == request.user


class IsInParticipantsInAdminsOrCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.participants.all() or obj.user == request.user or request.user in obj.admins.all()


class IsInAdminsOrCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.admins.all() or obj.user == request.user
