import logging

import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

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

            token = get_token(username, password)

            request.session['token'] = token
            return redirect('profile_user')
        else:
            logger.warning('Проверьте правильность данных для %s', username)
            return JsonResponse({'error':'Проверьте правильность данных'}, status=401)

    return render(request, 'authe/login.html')


def get_token(username, password):
    token_url = 'http://localhost:8000/auth/token/login'

    user_data = {
        'username': username,
        'password': password
    }
    logger.info('Попытка получения токена для %s', username)
    response = requests.post(token_url, json=user_data)
    if response.status_code == 200:
        logger.info('Токен для %s успешно получен', username)
        return response.json().get('auth_token', None)
    else:
        logger.warning('Ошибка получения токена для %s', username)
        return JsonResponse({'error':'Ошибка получения токена'}, status=500)


def logout(request):
    logout_url = 'http://127.0.0.1:8000/auth/token/logout/'
    token = request.session.get('token', '')
    headers = {'Authorization': f'Token {token}'}
    logger.info('Попытка выхода из аккаунта')
    response = requests.post(logout_url, headers=headers)

    if response.status_code == 204:
        auth_logout(request)
        logger.info('Вы разлогинились')
        return redirect('in')
    else:
        return JsonResponse({'error':'Ошибка выхода'}, status=500)


@validate_registration
def registration(request):
    if request.method == 'POST':
        registration_url = 'http://127.0.0.1:8000/auth/api/auth/users/'

        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            data = {
                'username': username,
                'password': password1,
            }
            logger.info('Попытка регистрации пользователя - %s', username)
            response = requests.post(registration_url, data=data)

            if response.status_code == 201:
                logger.info('Пользователь %s успешно зарегистрирован', username)
                return redirect('in')
            else:
                logger.warning('Ошибка регистрации %s', username)
                return JsonResponse({'error': 'Ошибка регистрации'}, status=400)

    return render(request, 'authe/registration.html')
