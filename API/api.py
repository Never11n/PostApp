from ninja import NinjaAPI, Form
from ninja.security import HttpBearer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .models import User
from .api_views import posts_router, comments_router, user_router
from secrets import compare_digest


class GlobalAuth(HttpBearer):

    def authenticate(self, request, token):
        return token if compare_digest(token, request.user.token) else JsonResponse({
            'access': False,
            'message': 'Not authorized'}, status=403)


api = NinjaAPI(auth=GlobalAuth())

api.add_router('/posts', posts_router)
api.add_router('/comments', comments_router)
api.add_router('/auto_answer', user_router)


@api.post("/register", auth=None)
def register(request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'access': False,
            'message': 'Username already exists'
        }, status=400)
    if compare_digest(password, confirm_password):
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return JsonResponse({
            'access': True,
            'message': 'User registered successfully'
        }, status=201)
    else:
        return JsonResponse({
            'access': False,
            'message': 'Passwords do not match'
        }, status=400)


@api.post("/token", auth=None)
def get_token(request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return {"token": user.token}
    JsonResponse({
        'access': False,
        'message': 'Not authorized'
    }, status=403)
