from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from accountapp.managers import CustomUserManager


class User(AbstractUser):
    name = models.CharField(max_length=255, )
    email = models.EmailField(unique=True, null=False, )
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, )

    activation_key = models.CharField(max_length=150, blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True, )
    status = models.BooleanField(default=True, )

    username = None
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')






