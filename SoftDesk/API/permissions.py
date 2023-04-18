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
        print(request.method)
        if request.method not in ["PUT", "PATCH", "DELETE"]:
            return True

        owner = obj.author_user_id
        return owner == request.user


class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(obj, Project):
            contribution = Contributor.objects.filter(
                user_id=request.user,
                project_id=obj
            ).exists()

        if (obj.author_user_id == request.user or contribution):
            return True

        return False
