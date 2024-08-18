import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
from .tasks import auto_send_comment_with_delay


@receiver(post_save, sender=Comment)
def comment_auto_answer(sender, instance, created, **kwargs):
    if created and not instance.parent and instance.author.enabled_auto_answer:
        user = instance.author
        delay = user.auto_answer_delay * 60
        auto_send_comment_with_delay.apply_async(args=[instance.id], countdown=delay)
