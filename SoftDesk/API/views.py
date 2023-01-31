from rest_framework import permissions, viewsets
from rest_framework.response import Response
from API.serializers import ProjectSerializer, ContributorsSerializer, IssueSerializer, CommentSerializer
from API.models import Project, Contributor, Issue, Comment


class ProjectViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.author_user_id = request.user.id
        if serializer.is_valid():
            serializer.save()
            print(serializer, "Ok")
            return Response(True)
        
        else:
            print(serializer, "No No")
            return Response(serializer.errors)
        

class ContributorViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Contributor.objects.all()
    serializer_class = ContributorsSerializer


class IssueViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class CommentViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
