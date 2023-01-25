from django.urls import include, path
from django.contrib import admin
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from API.views import ProjectViewset


router = routers.SimpleRouter()
router.register("projects", ProjectViewset, basename='projects')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('', include(router.urls)),
    path('', include('rest_framework.urls'))
]