from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):

    def authenticate(self, request, token):
        return token if token == request.user.token else JsonResponse({
                                                        'access': False,
                                                        'message': 'Not authorized'},status=403)
