from __future__ import unicode_literals

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, AnonymousUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from django.db.models.fields import CharField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user."""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email instead of username."""

    email = models.EmailField(max_length=120, unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=128, blank=True)
    price = models.PositiveIntegerField()
    file = models.ImageField(upload_to='images/')

    
    def __str__(self):
        return self.name
