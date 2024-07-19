import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .services import AuthService
from .validators import validate_login, validate_registration

logger = logging.getLogger(__name__)


@validate_login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info('Попытка входа пользователя - %s', username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.info('Пользователь %s успешно авторизован', username)
            auth_login(request, user)

            token = AuthService.get_token(username, password)

            if token:
                request.session['token'] = token
                return redirect('profile_user')
            else:
                return JsonResponse({'error': 'Ошибка получения токена'}, status=500)
        else:
            logger.warning('Проверьте правильность данных для %s', username)
            return JsonResponse({'error': 'Проверьте правильность данных'}, status=401)

    return render(request, 'authe/login.html')


def logout(request):
    token = request.session.get('token', '')
    if AuthService.logout(token):
        auth_logout(request)
        logger.info('Вы разлогинились')
        return redirect('in')
    else:
        return JsonResponse({'error': 'Ошибка выхода'}, status=500)


@validate_registration
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')

        response = AuthService.register(username, password1)

        if response.status_code == 201:
            logger.info('Пользователь %s успешно зарегистрирован', username)
            return redirect('in')
        else:
            logger.warning('Ошибка регистрации %s', username)
            return JsonResponse({'error': 'Ошибка регистрации'}, status=400)

    return render(request, 'authe/registration.html')
