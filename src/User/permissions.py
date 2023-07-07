from rest_framework import permissions


class UserUpdatePermission(permissions.BasePermission):
    """
    Permission for check if the logged user can update account, profile, passowrd.
    User can update own account, profile, passowrd.
    """
    def has_permission(self, request, view):
        if request.user == view.get_object():
            return True
        
        return False