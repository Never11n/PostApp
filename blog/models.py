import jwt
import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.IntegerField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        datetime_tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        message = {'id': self.pk,
                   'exp': datetime_tomorrow
                   }
        token = jwt.encode(message, settings.SECRET_KEY, algorithm='HS256')
        return token

