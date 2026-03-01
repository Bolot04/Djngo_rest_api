from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get("phone_number"):
            return ValueError("Superuser must have a phone number.")
        
        return super().create_superuser(username, email, password, **extra_fields)
    
       