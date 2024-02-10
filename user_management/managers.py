# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

    def authenticate(username=None, password=None, manager=None):

        if not username or not password or not manager:
            return None

        try:
            user = manager.get(username=username)
        except manager.model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
