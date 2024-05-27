from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from equipment.models import UserEquipment
from front.forms import EquipmentForm, UserEquipmentForm


def get_equipment(request):
    api_url = 'http://127.0.0.1:8000/api/equipment/'

    try:
        token = request.session.get('token', '')
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(api_url,headers=headers)
        response.raise_for_status()

        data = response.json()
        return render(request, 'equipment_list.html', {'data': data})

    except Exception as e:
        return HttpResponse(f'Ошибка: {e}')


def post_equipment(request):
    api_url = 'http://127.0.0.1:8000/api/equipment/'
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():

            data = {
                'name': form.cleaned_data['name'],
                'inventory_number': form.cleaned_data['inventory_number'],
                'nomenclature_number': form.cleaned_data['nomenclature_number']
            }
            token = request.session.get('token', '')
            headers = {'Authorization': f'Token {token}'}
            response = requests.post(api_url, data=data, headers=headers)

            if response.status_code == 201:
                return redirect('equipment_list')
            else:
                return HttpResponse(f"Error: {response.status_code} - {response.text}")
    else:
        form = EquipmentForm()

    return render(request, 'post_equipment.html', {'form': form})


def user_equipment(request):
    if request.method == 'POST':
        form = UserEquipmentForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user'].id
            equipment_data = {
                'name': form.cleaned_data['name'],
                'inventory_number': form.cleaned_data['inventory_number'],
                'nomenclature_number': form.cleaned_data['nomenclature_number']
            }
            data = {
                'user': user_id,
                'equipment': equipment_data
            }
            token = request.session.get('token', '')
            headers = {'Authorization': f'Token {token}'}
            response = requests.post('http://127.0.0.1:8000/api/user/equipment/', json=data,
                                     headers=headers)

            if response.status_code == 201:
                return redirect('user_equipment')
            else:
                return HttpResponse(f"Error: {response.status_code} - {response.text}")
    else:
        form = UserEquipmentForm()

    data = UserEquipment.objects.all()

    return render(request, 'user_equipment.html', {'form': form, 'data': data})


def profile_user(request):
    user_id = request.user.id
    try:
        token = request.session.get('token', '')
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f'http://127.0.0.1:8000/api/profile/{user_id}/', headers=headers)
        response.raise_for_status()
        data = response.json()
        equipment_list = [item['equipment'] for item in data]
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: {e}")

    return render(request, 'profile.html', {'data': equipment_list})

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