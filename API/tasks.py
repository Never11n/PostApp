from celery import shared_task
from django.http import JsonResponse

from .models import Comment
from .google_ai import send_prompt


@shared_task
def auto_send_comment_with_delay(comment, post):
    try:
        prompt = (f'Answer on this commentary relative to the comment and post.'
                  f'Post:{post.content}; '
                  f'Comment:{comment.content}. '
                  f'You must return plain text')
        response = send_prompt(prompt)
        Comment.objects.create(post=post, content=response, parent=comment, author=post.author, blocked=False)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)})