from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from uuid import uuid4


class CustomUser(AbstractBaseUser):
    _id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=50)
    auth0_user_id = models.CharField(max_length=128, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    db_table = "users"
    indexes = [
        models.Index(fields=["email", "id"]),
    ]

    def __str__(self):
        return self.email

