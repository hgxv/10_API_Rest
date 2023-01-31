from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Project(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Issue(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    