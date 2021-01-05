from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,\
    PermissionsMixin


class CustomUserManager(BaseUserManager):
    """CUSTOM USER MANAGER"""
    def create_user(self, email, password=None,
                    first_name=None, last_name=None):
        """
        Creates and saves a user with the given email, first_nam,
        last_name, password.
        """
        if not email:
            raise ValueError('Enter a valid email address')

        user = self.model(first_name=first_name, last_name=last_name,
                          email=email)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User table with base user"""
    country_choices = (
        ('INDIA', 'INDIA'),
        ('USA', 'USA')
    )

    first_name = models.CharField(max_length=50, null=True, db_index=True)
    last_name = models.CharField(max_length=50, null=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    country = models.CharField(max_length=15, choices=country_choices, null=True, db_index=True)
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
