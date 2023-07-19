from rest_framework import permissions


class PostOwnerPermission(permissions.BasePermission):
    """
    Permission that any user can create obj (POST method) but only owners of the specific obj can access it to update or delete.
    """

    SAFE_METHODS = "POST"

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return True

        if request.user == obj.user:
            return True

        return False
