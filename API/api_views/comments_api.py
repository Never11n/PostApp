from django.http import JsonResponse

from ninja import Router, Form

from ..schemas import CommentIn, CommentOut
from ..models import Comment
from ..google_ai import send_prompt

router = Router()


@router.post('/leave-a-comment/{post_id}', response=CommentOut)
def leave_a_comment(request, post_id: int, data: Form[CommentIn]):
    try:
        content = data.content
        response = send_prompt(
            f"Return True if text has no obscene language and abusive language.You must send only True or False:{content}")
        blocked = False if 'True' in response else True
        comment = Comment.objects.create(post_id=post_id, **data.dict(), author=request.user, blocked=blocked)
        return {
            'id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'blocked': comment.blocked
        }
    except Exception as e:
        return JsonResponse({'error': str(e)})
