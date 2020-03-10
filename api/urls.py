

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter


from . import views

router = DefaultRouter()
router.register(r'files', views.FilesViewSet, basename='files')
router.register(r'places', views.PlacesViewSet, basename='places')

urlpatterns = [
    path('signup', views.sign_up_user),
    path('profile', views.profile),
    path('app_init', views.app_init_data),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls