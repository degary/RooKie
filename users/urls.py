from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .login_views import LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]