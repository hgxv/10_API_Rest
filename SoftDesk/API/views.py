from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from API.serializers import ProjectSerializer, ContributorsSerializer,\
 IssueSerializer, CommentSerializer, CreateUserProfileSerializer
from API.models import Project, Contributor, Issue, Comment, User
from API.permissions import IsOwnerOrReadOnly, IsContributor
from django.db.models import Q

from django.utils import timezone


class ProjectViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly, IsContributor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        contributions = list(Contributor.objects.filter(user_id=request.user))
        projects = [project.project_id.id for project in contributions]
        queryset = Project.objects.filter(
            Q(author_user_id=request.user) | Q(id__in=projects)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(request, project)
            serializer = self.serializer_class(project)
            return Response(serializer.data)
        
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(request, project)
            serializer = self.serializer_class(
                instance=project,
                data=request.data,
                partial=True)

            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)

            else:
                return Response(serializer.errors)
            
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(request, project)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ContributorViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly, IsContributor]
    serializer_class = ContributorsSerializer

    def list(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Contributor.objects.filter(project_id=project.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            contribution = Contributor.objects.filter(
                user_id=serializer.validated_data["user_id"],
                project_id=project
            ).exists()
            if contribution:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer.save(project_id=project)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def destroy(self, request, project_pk, pk=None):
        try:
            project = Project.objects.get(pk=project_pk)
            self.check_object_permissions(request, project)
            contribution = Contributor.objects.get(
                user_id=pk,
                project_id=project_pk
            )
            contribution.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IssueViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly, IsContributor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def list(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Issue.objects.filter(project_id=project.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        serializer = self.serializer_class(
            data=request.data, context={'resquest': request}
        )
        self.check_object_permissions(request, project)
        if serializer.is_valid():
            user = serializer.validated_data["assignee_user_id"]
            contribution = Contributor.objects.filter(
                user_id=user,
                project_id=project
            ).exists()

            if contribution or user == request.user:
                serializer.save(
                    project_id=project,
                    author_user_id=request.user,
                    created_time=timezone.now()
                )
                return Response(serializer.data)
            
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(serializer.errors)

    def update(self, request, project_pk, pk=None):
        try:
            project = Project.objects.get(pk=project_pk)
            issue = Issue.objects.get(pk=pk)
            self.check_object_permissions(request, project)
            serializer = self.serializer_class(
                instance=issue,
                data=request.data,
                partial=True
                )

            if serializer.is_valid():
                user = serializer.validated_data["assignee_user_id"]
                contribution = Contributor.objects.filter(
                    user_id=user,
                    project_id=project
                ).exists()
                if contribution or user == request.user:
                    self.perform_update(serializer)
                    return Response(serializer.data)
                
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)

            else:
                return Response(serializer.errors)
        
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, project_pk, pk=None):
        try:
            project = Project.objects.get(pk=project_pk)
            self.check_object_permissions(request, project)
            issue = Issue.objects.filter(
                pk=pk,
                project_id=project_pk
            )
            issue.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly, IsContributor]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, project_pk, issues_pk):
        issue = Issue.objects.get(pk=issues_pk)
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Comment.objects.filter(issue_id=issue.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk, issues_pk):
        issue = Issue.objects.get(pk=issues_pk)
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author_user_id=request.user,
                issue_id=issue,
                created_time=timezone.now()
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def retrieve(self, request, project_pk, issues_pk, pk=None):
        try:
            project = Project.objects.get(pk=project_pk)
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, project)
            serializer = self.serializer_class(comment)
            return Response(serializer.data)
        
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, project_pk, issues_pk, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            serializer = self.serializer_class(
                instance=comment,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                return self.perform_update(serializer)

            else:
                return Response(serializer.errors)
        
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, project_pk, issues_pk, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SignupViewset(viewsets.ViewSet):

    @action(detail=False, methods=["POST"])
    def signup(self, request):

        serializer = CreateUserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
