from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, max_length=128, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
