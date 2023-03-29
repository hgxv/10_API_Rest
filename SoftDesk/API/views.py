from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from API.serializers import ProjectSerializer, ContributorsSerializer,\
 IssueSerializer, CommentSerializer, CreateUserProfileSerializer
from API.models import Project, Contributor, Issue, Comment
from API.permissions import IsOwnerOrReadOnly, IsContributor
from django.db.models import Q

from django.utils import timezone

class ProjectViewset(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def list(self, request):
        contributions = list(Contributor.objects.filter(user_id=request.user))
        projects = [project.project_id.id for project in contributions]

        queryset = Project.objects.filter(
            Q(author_user_id=request.user) | Q(id__in=projects)
        )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @permission_classes[IsContributor]
    def retrieve(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        self.check_object_permissions(request, request.user)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        
    def partial_update(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        project.update()

    def destroy(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    serializer_class = ContributorsSerializer

    def list(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        queryset = Contributor.objects.filter(project_id=project.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk):
        project = Project.objects.filter(pk=project_pk)
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(project_id=project[0])
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
    
    def destroy(self, request, project_pk, pk=None):
        user = Contributor.objects.get(
            user_id=pk,
            project_id=project_pk
        )
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def create(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        serializer = self.serializer_class(
            data=request.data, context={'resquest': request}
        )

        if serializer.is_valid():
            serializer.save(
                project_id = project,
                created_time = timezone.now()
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def retrieve(self, request, project_pk=None):
        pass

class CommentViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SignupViewset(viewsets.ViewSet):

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        
        serializer = CreateUserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
