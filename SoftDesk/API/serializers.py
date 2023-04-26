from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

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
        username = data["first_name"][0].casefold() + "." + data["last_name"].casefold()
        username = self.check_username(username)

        user = User.objects.create_user(
            username, data["email"], data["password"]
        )

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
        return user

    def check_username(self, username, NextId=1):
        if User.objects.filter(username=username + str(NextId)).exists():
            NextId += 1
            return self.check_username(username, NextId)

        else:
            username += str(NextId)
            return username
