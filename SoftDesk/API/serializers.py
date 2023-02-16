from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from API.models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class ContributorsSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
        
        
class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CreateUserProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


    def create(self, data):
        username = data["first_name"]+ "." + data["last_name"]
        username = self.check_username(username, 1)
        
        user = User.objects.create_user(
            username, data["email"], data["password"]
        )

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
        return user


    def check_username(self, username, NextId):
        if User.objects.filter(username=username + str(NextId)).exists():
            NextId += 1
            return self.check_username(username, NextId)
        
        else:
            username += str(NextId)
            return username
