from celery import shared_task
from django.http import JsonResponse

from .models import Comment
from .google_ai import send_prompt


@shared_task
def auto_send_comment_with_delay(comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    try:
        prompt = (f'Answer on this commentary relative to the comment and post.'
                  f'Post:{post.content}; '
                  f'Comment:{comment.content}. '
                  f'You must answer like a author of this post')
        response = send_prompt(prompt)
        Comment.objects.create(post=post, content=response, parent=comment, author=post.author, blocked=False)
        return {'success': True}
    except Exception as e:
        return JsonResponse({'error': str(e)})