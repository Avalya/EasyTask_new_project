from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ApplicationViewSet,
    DepartmentPanelView,
    CustomTokenObtainPairView,
    assign_application
)

# ✅ Router for Application ViewSet
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')

# ✅ URL patterns
urlpatterns = [
    path('', include(router.urls)),                                     # /api/applications/
    path('department/', DepartmentPanelView.as_view()),                # /api/department/
    path('token/', CustomTokenObtainPairView.as_view(), name='token'), # /api/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # /api/token/refresh/
    path('assign/', assign_application, name='assign_application'),    # /api/assign/
]
