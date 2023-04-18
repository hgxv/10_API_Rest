from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Project(models.Model):

    TYPE_CHOICES = [
        ("0", "BACK-END"),
        ("1", "FRONT-END"),
        ("2", "iOS"),
        ("3", "ANDROID")
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Issue(models.Model):

    PRIORITY_CHOICES = [
        ("0", "FAIBLE"),
        ("1", "MOYENNE"),
        ("2", "ÉLEVÉE")
    ]

    BALISE_CHOICES = [
        ("0", "BUG"),
        ("1", "AMÉLIORATION"),
        ("2", "TÂCHE")
    ]

    STATUT_CHOICES = [
        ("0", "À FAIRE"),
        ("1", "EN COURS"),
        ("2", "TERMINÉ")
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=1, choices=BALISE_CHOICES)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUT_CHOICES)
    author_user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="author")
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(null=True)


class Comment(models.Model):
    
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(null=True)


class Contributor(models.Model):

    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
