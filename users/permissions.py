from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return obj.user == request.user


class IsInParticipants(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.participants.all()


class IsInAdmins(BasePermission):
    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user in obj.admins.all()
