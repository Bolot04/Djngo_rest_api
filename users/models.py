from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.email






class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.user.email} - {self.code}'