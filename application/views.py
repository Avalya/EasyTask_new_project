from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import io
import xlsxwriter

from .models import Application
from .serializers import ApplicationSerializer


# 🔐 Custom JWT Serializer with extra user claims
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['groups'] = list(user.groups.values_list('name', flat=True))
        token['role'] = 'admin' if user.is_superuser else 'department'
        return token


# 🔐 Custom JWT View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 🔁 Admin assigns application to a user
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def assign_application(request):
    app_id = request.data.get('id')
    user_id = request.data.get('user_id')

    if not app_id or not user_id:
        return Response({'error': 'Both application ID and user ID are required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        app = Application.objects.get(id=app_id)
        user = User.objects.get(id=user_id)
        app.assigned_to = user
        app.save()
        return Response({'success': 'Assigned successfully'})
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# 📄 Application ViewSet
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='admins').exists():
            return Application.objects.all().order_by('-submitted_at')
        elif user.groups.filter(name='departments').exists():
            return Application.objects.filter(assigned_to=user).order_by('-submitted_at')
        return Application.objects.none()

    @action(detail=False, methods=['get'], url_path='status/(?P<reg_number>[^/.]+)')
    def check_status(self, request, reg_number=None):
        application = get_object_or_404(Application, reg_number=reg_number)
        return Response({'status': application.status})

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        applications = self.get_queryset()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        headers = ["ID", "Full Name", "Status"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for row, app in enumerate(applications, start=1):
            worksheet.write(row, 0, app.id)
            worksheet.write(row, 1, app.full_name)
            worksheet.write(row, 2, app.status)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=applications.xlsx'
        return response


# 🏢 Department View
class DepartmentPanelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = Application.objects.filter(assigned_to=request.user)
        serializer = ApplicationSerializer(apps, many=True)
        return Response(serializer.data)

    def patch(self, request):
        app_id = request.data.get('id')
        if not app_id:
            return Response({'error': 'Application ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = Application.objects.get(id=app_id, assigned_to=request.user)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ApplicationSerializer(app, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
