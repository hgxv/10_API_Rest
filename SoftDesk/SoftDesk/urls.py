from django.urls import include, path
from django.contrib import admin

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from API.views import ProjectViewset, ContributorViewset, IssueViewset,\
    CommentViewset, SignupViewset


router = routers.SimpleRouter()
router.register("projects", ProjectViewset, basename='projects')
router.register("", SignupViewset, basename="signup")

project_router = routers.NestedSimpleRouter(router, "projects", lookup="project")
project_router.register("users", ContributorViewset, basename='user')
project_router.register("issues", IssueViewset, basename='issue')

issues_router = routers.NestedSimpleRouter(project_router, "issues", lookup="issues")
issues_router.register("comments", CommentViewset, basename="comment")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issues_router.urls)),
    path('', include('rest_framework.urls'))
]