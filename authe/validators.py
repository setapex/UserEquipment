from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
def validate_login(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                logger.warning('Username и password необходимо заполнить')
                return JsonResponse({'error': 'Username и password необходимо заполнить'}, status=400)

        return func(request, *args, **kwargs)
    return wrapper

def validate_registration(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if not username or not password1 or not password2:
                logger.warning('Все поля необходимо заполнить')
                return JsonResponse({'error': 'Все поля необходимо заполнить'}, status=400)

            if password1 != password2:
                logger.warning('Пароли не совпадают')
                return JsonResponse({'error': 'Пароли не совпадают'}, status=400)

            if len(password1) < 8:
                logger.warning('Минимальная длина пароля - 8 символов')
                return JsonResponse({'error': 'Минимальная длина пароля - 8 символов'}, status=400)

        return func(request, *args, **kwargs)
    return wrapper