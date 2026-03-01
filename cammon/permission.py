from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self,request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method == 'POST' and request.user.is_staff:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        owner = getattr(obj, 'owner', None)
        return owner == request.user