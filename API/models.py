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



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('blog.User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('blog.User', on_delete=models.CASCADE, related_name="comments")
    blocked = models.BooleanField(default=False)
