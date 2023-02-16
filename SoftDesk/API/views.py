from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from API.serializers import ProjectSerializer, ContributorsSerializer,\
 IssueSerializer, CommentSerializer, CreateUserProfileSerializer
from API.models import Project, Contributor, Issue, Comment


class ProjectViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


    def create(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        

class ContributorViewset(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContributorsSerializer

    def list(self, request, project_pk):
        project = Project.objects.filter(pk=project_pk)
        queryset = Contributor.objects.filter(project_id=project[0].id)
        print(queryset)
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


class IssueViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


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
