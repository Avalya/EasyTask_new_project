from django.db import models
from django.contrib.auth.models import User
import uuid

# Типы заявлений
APPLICATION_TYPES = [
    ('request', 'Request'),
    ('complaint', 'Complaint'),
    ('feedback', 'Feedback'),
]

# Департаменты
DEPARTMENTS = [
    ('education', 'Education'),
    ('health', 'Health'),
    ('finance', 'Finance'),
]

class Application(models.Model):
    reg_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    app_type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    message = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

  
    department = models.CharField(max_length=50, choices=DEPARTMENTS, default='education')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_apps')

    def __str__(self):
        return f'{self.full_name} ({self.reg_number})'
