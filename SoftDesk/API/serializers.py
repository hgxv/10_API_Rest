from django.contrib.auth.models import User, Group
from rest_framework import serializers

from API.models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
