from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from backend.core.validators.password import (
    validate_min_digits_3, 
    validate_min_length_8, 
    validate_min_non_alphanumeric_1, 
    validate_min_uppercase_1
)

import uuid

class UserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, password=None, **kwargs):

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, first_name, last_name, password=None, **kwargs):
        return self._create_user(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            is_staff=False,
            is_superuser=False,
            **kwargs
        )
    
    def create_superuser(self, email, first_name, last_name, password=None, **kwargs):
        return self._create_user(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            is_staff=True,
            is_superuser=True,
            **kwargs
        )

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    username = models.CharField(
        max_length=255, 
        unique=True, 
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=255, 
        unique=True, 
        null=False, 
        blank=False
    )
    password = models.CharField(max_length=128, validators=[
        validate_min_length_8,
        validate_min_uppercase_1,
        validate_min_digits_3,
        validate_min_non_alphanumeric_1
    ])
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]