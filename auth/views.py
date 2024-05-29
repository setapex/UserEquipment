from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import requests

from front.views import profile_user
def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            token = get_token(username, password)

            request.session['token'] = token
            return profile_user(request)
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')

def get_token(username, password):
    token_url = 'http://localhost:8000/auth/token/login'

    user_data = {
        'username': username,
        'password': password
    }
    response = requests.post(token_url, json=user_data)
    if response.status_code == 200:
        return response.json().get('auth_token', None)
    else:
        return None


def logout(request):
    logout_url = 'http://127.0.0.1:8000/auth/token/logout/'
    token = request.session.get('token', '')
    headers = {'Authorization': f'Token {token}'}

    response = requests.post(logout_url, headers=headers)

    if response.status_code == 204:
        auth_logout(request)
        return redirect('/login')
    else:
        return HttpResponse(f"Ошибка выхода: {response.status_code} - {response.text}")