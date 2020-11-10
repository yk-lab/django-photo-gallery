from __future__ import annotations

from typing import Optional, cast

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


class UserManager(BaseUserManager):
    def create_user(
            self,
            username: str,
            password: Optional[str] = None) -> User:
        if not username:
            raise ValueError('Users must have an user name')

        user = cast(User, self.model(username=username))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username: str,
            password: Optional[str] = None) -> User:
        """
        Creates and saves a superuser with the given user name and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, UUIDModel, TimeStampedModel):
    username = models.CharField(
        verbose_name='ユーザ名',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, label):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
