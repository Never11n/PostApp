from datetime import datetime

from ninja import Router, Form

from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from ..models import Post
from ..schemas import PostIn, PostOut

router = Router()


# All from this functions should be in class (by my reasons), but I had an issue with self argument requiring in api docs

@router.post('/create-post/', response=PostOut)
def create_post(request, data: Form[PostIn]):
    try:
        author = request.user
        post = Post.objects.create(
            title=data.title,
            content=data.content,
            author=author,
        )
        return {
            'id': post.id,
            'author': post.author.username,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at
        }
    except ValueError:
        return JsonResponse({'access': False, 'message': 'Invalid data'}, status=400)
