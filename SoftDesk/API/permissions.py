from rest_framework import permissions
from API.models import Project, Contributor


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
            
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = obj.author_user_id.id
        return owner == request.user.id
    

class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        contribution = Contributor.objects.filter(
            user_id=request.user,
            project_id=obj
        ).exists()

        if (obj.author_user_id.id != request.user.id and
            contribution == False):
            
            print(obj.author_user_id, " ", request.user.id)
            return False
        
        if (view.action == "destroy" and
            obj.author_user_id.id != request.user.id):
            
            return False
        
        return True
