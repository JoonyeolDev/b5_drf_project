from rest_framework import permissions 
class IsAdminUserOrReadonly(permissions.BasePermission):
    # has_permission
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user and request.user.is_admin
    
    # has_object_permission
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin
    
class IsAuthorOrReadonly(permissions.BasePermission):
    # has_permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    # has_object_permission
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user