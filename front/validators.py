from django.http import JsonResponse

def validate_auth(func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('token', '')
        if not token:
            return JsonResponse({'error':"Ошибка авторизации"}, status=403)
        return func(request, *args, **kwargs)
    return wrapper

