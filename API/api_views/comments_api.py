import asyncio

from datetime import datetime

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ninja import Router, Form

from ..schemas import CommentIn, CommentOut
from ..models import Comment, Post
from ..google_ai import check_comment, send_prompt

router = Router()


@router.post('/leave-a-comment/{post_id}', response=CommentOut)
def leave_a_comment(request, post_id: int, data: Form[CommentIn]):
    try:
        if not data.content:
            raise ValueError
        content = data.content
        blocked = check_comment(content)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(post=post, **data.dict(), author=request.user, blocked=blocked)
        return {
            'id': comment.id,
            'author': comment.author,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'blocked': comment.blocked,
        }
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Invalid data'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@router.post('/reply/{comment_id}')
def reply_to_comment(request, comment_id: int, data: Form[CommentIn]):
    try:
        parent_comment = Comment.objects.get(id=comment_id)
        content = data.content
        blocked = check_comment(content)
        comment = Comment.objects.create(post=parent_comment.post,
                                         **data.dict(),
                                         author=request.user,
                                         blocked=blocked,
                                         parent=parent_comment)
        return CommentOut.from_orm(comment)

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)


@router.get('/daily-breakdown')
def comments_daily_breakdown(request, date_from: datetime, date_to: datetime):
    try:
        date_to = date_to if date_to <= datetime.now() else datetime.now()
        date_to = date_to.replace(hour=23)
        comments_count = Comment.objects.filter(created_at__range=(date_from, date_to)).count()
        comments_by_date = (Comment.objects.filter(created_at__range=(date_from, date_to))
                            .annotate(date=TruncDate('created_at'))
                            .values('date')
                            .annotate(total_count=Count('id'),
                                      normal_comments_count=Count('id', filter=Q(blocked=False)),
                                      blocked_comments_count=Count('id', filter=Q(blocked=True))
                                      )
                            .order_by('date')
                            )
        return JsonResponse({
            'total_comments': comments_count,
            'comments': [comment for comment in comments_by_date]
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

