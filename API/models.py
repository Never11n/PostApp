from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    blocked = models.BooleanField(default=False)
