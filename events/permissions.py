from  rest_framework.permissions import BasePermission , SAFE_METHODS


class IsOwnerOrReadonly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in  SAFE_METHODS: return True

        return obj.organizer == request.user



