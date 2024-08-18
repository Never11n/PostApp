from ninja import Router

from django.http import JsonResponse

router = Router()


@router.patch('/enable-auto-answer')
def enable_auto_answer(request, auto_answer_delay: int) -> JsonResponse:
    user = request.user
    user.enabled_auto_answer = True
    user.auto_answer_delay = auto_answer_delay
    user.save()
    return JsonResponse({'success': True, 'answer_delay': f"{user.auto_answer_delay} minutes"})


@router.patch('/disable-auto-answer')
def disable_auto_answer(request) -> JsonResponse:
    user = request.user
    user.enabled_auto_answer = False
    user.save()
    return JsonResponse({'success': True})
