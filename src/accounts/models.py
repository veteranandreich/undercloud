from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email and not password and not username:
            raise ValueError('Users must have an username, email and password')
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None:
            raise ValueError('Superusers must have a password.')
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, db_index=True, unique=True)
    email = models.EmailField(unique=True)
    date_of_registration = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username
