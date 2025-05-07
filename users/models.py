from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Roles
ROLE_CHOICES = (
    ('client', 'Client'),
    ('admin', 'Admin'),
    ('professional', 'Professional'),
)

# Status for Professional registration
STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('canceled', 'Canceled'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, birth_date, phone, role, password=None, **extra_fields):
        """
        Create and return a regular user with an email, full name, birth date, phone, and role.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, birth_date=birth_date, phone=phone, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, birth_date, phone, role, password=None, **extra_fields):
        """
        Create and return a superuser with the given email, full name, birth date, phone, role, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, birth_date, phone, role, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove username since we use email
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Custom manager for handling user creation and superuser creation
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'birth_date', 'phone', 'role']

    def is_client(self):
        return self.role == 'client'

    def is_professional(self):
        return self.role == 'professional'

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    card_number = models.CharField(max_length=16)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Professional {self.user.full_name} ({self.status})"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')

    def __str__(self):
        return f"Client {self.user.full_name}"
