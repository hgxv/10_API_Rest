from django.contrib import admin

from API.models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'type', 'author_user_id')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'author_user_id', 'assignee_user_id')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('issue_id', 'author_user_id', 'description')


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('user_id', 'project_id', 'permission', 'role')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
