from rest_framework import permissions 

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # try to get object owner || user 
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        if owner is None:
            raise TypeError("Given object is not related to user model")
        return request.user.pk == owner.pk

