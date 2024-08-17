import jwt
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.conf import settings
from django.db import models


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    enabled_auto_answer = models.BooleanField(default=True)

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
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def __repr__(self):
        return "Post({title}, {author}, {created_at})".format(
            title=self.title,
            author=self.author.username,
            created_at=self.created_at
        )


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}- {self.content[:50]}"

