from rest_framework import permissions, viewsets
from API.serializers import ProjectSerializer
from API.models import Project


class ProjectViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
