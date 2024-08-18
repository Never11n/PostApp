from datetime import datetime

from ninja import Router, Form

from django.http import JsonResponse
from django.db.models import Prefetch, Count

from ..models import Post, Comment
from ..schemas import PostIn, PostOut, CommentOut

router = Router()


# All from this functions should be in class (by my reasons), but I had an issue with self argument requiring in api docs

@router.post('/create-post/', response=PostOut)
def create_post(request, data: Form[PostIn]):
    try:
        print(data.title, data.content)
        if not data.title or not data.content:
            print('in')
            raise ValueError
        author = request.user
        post = Post.objects.create(
            title=data.title,
            content=data.content,
            author=author,
        )
        return {
            'id': post.id,
            'author': post.author,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at
        }
    except ValueError as e:
        print(e)
        return JsonResponse({'message': 'Invalid data'}, status=403)


@router.get('/')
def get_posts(request) -> list[PostOut]:
    filtered_comments = Comment.objects.filter(blocked=False, parent=None)
    posts = Post.objects.prefetch_related(
        Prefetch('comments', queryset=filtered_comments),
        'comments__replies').all()
    posts_count = {'post_count': posts.count()}
    formatted_posts = [PostOut.from_orm(post) for post in posts]
    formatted_posts.insert(0, posts_count)
    return formatted_posts
