from datetime import datetime

from ninja import Router, Form

from django.http import JsonResponse

from ..models import Post
from ..schemas import PostIn, PostOut

router = Router()

# All from this functions should be in class (by my reasons), but I had an issue with self requiring in api docs

@router.post('/create-post/', response=PostOut, auth=None)
def create_post(request, data: Form[PostIn]):
    try:
        author = request.user
        created_at = datetime.now()
        post = Post.objects.create(
            title=data.title,
            content=data.content,
            author=author,
            created_at=created_at
        )
        return post
    except Exception as e:
        return JsonResponse({'error': e})
