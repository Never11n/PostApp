from ninja import NinjaAPI, Form
from ninja.security import HttpBearer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import User
from .api_views.post_api import router as post_router


class GlobalAuth(HttpBearer):

    def authenticate(self, request, token):
        return token if token == request.user.token else JsonResponse({
            'access': False,
            'message': 'Not authorized'}, status=403)


api = NinjaAPI(auth=GlobalAuth())

api.add_router('/posts', post_router)

@api.post("/token", auth=None)
def get_token(request, username: str = Form(...), password: str = Form(...)):
        user = authenticate(username=username, password=password)
        return {"token": user.token} if user is not None else JsonResponse({
            'access': False,
            'message': 'Not authorized'
        }, status=403)

