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

        # Instance must have an attribute named `id`.
        owner = obj.project_id.author_user_id.id
        return owner == request.user.id


class IsContributor(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        contributions = list(Contributor.objects.filter(user_id=request.user))
        projects = [project.project_id.id for project in contributions]

        print(request.project)

        if self.pk not in projects:
            return False
        
        return True
