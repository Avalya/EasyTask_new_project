# application/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApplicationViewSet,
    DepartmentPanelView,
    CustomTokenObtainPairView,
    assign_application  # ✅ ВАЖНО: импортируем функцию назначения заявки
)
from rest_framework_simplejwt.views import TokenRefreshView

# ✅ Роутер для ViewSet
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')

# ✅ Основной список маршрутов
urlpatterns = [
    path('', include(router.urls)),                             # /api/applications/
    path('department/', DepartmentPanelView.as_view()),         # /api/department/
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token'),        # /api/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # /api/token/refresh/
    path('assign/', assign_application, name='assign_application'),                  # /api/assign/
]
