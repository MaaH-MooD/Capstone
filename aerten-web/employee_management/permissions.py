from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.employee.access_level in ['Admin', 'Manager']
    

class IsAdminManagerOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all authenticated users to access the view
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Allow admins/managers to perform any action
        if user.is_staff or user.employee.access_level in ["Admin", "Manager"]:
            return True

        # Allow the request owner to view their own requests (regardless of status)
        if view.action in ["retrieve", "list"]:
            return obj.employee.user == user

        # Allow the request owner to delete their own requests only if the request is in the "Pending" state
        if view.action == "destroy":
            return obj.employee.user == user and obj.status == "Pending"

        # Deny by default
        return False