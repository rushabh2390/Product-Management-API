from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager
from datetime import datetime
from django.contrib.auth.hashers import make_password
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)

    def get_queryset(self):
        """
        Getting queryset function for Soft Delete models.
        """
        return super().get_queryset().filter(deleted__isnull=True)


class CustomerUser(User):
    name = models.CharField(max_length=100, null=True,
                            blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True,blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    objects = UserManager()
    all_objects = models.Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.email

    def save(self, *args, **kwargs):
        # Check if already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)  # hash if not hashed
        self.is_active = True
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted = datetime.now()
        self.is_active = False
