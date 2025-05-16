from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse


def home(request):
    return HttpResponse("✅ Welcome to the SED (Document Management System) API.")

urlpatterns = [
    path('', home),  
    path('admin/', admin.site.urls),  # 🔐 Django 
    path('api/', include('application.urls')),  # 🧾 API 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 🔑 JWT логин
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 🔄 JWT refresh
]
