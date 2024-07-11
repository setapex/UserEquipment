
from django.http import HttpResponse
from django.shortcuts import render, redirect



from equipment.models import UserEquipment
from front.forms import EquipmentForm, UserEquipmentForm

from front.services import *


def get_equipment(request):
    try:
        token = request.session.get('token', '')
        if not token:
            return HttpResponse("Ошибка авторизации.", status=403)

        data = EquipmentService.get_equipment_data(token)
        return render(request, 'equipment/equipment_list.html', {'data': data})

    except Exception as e:
        return HttpResponse(f'Ошибка: {e}')


def post_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'inventory_number': form.cleaned_data['inventory_number'],
                'nomenclature_number': form.cleaned_data['nomenclature_number']
            }
            token = request.session.get('token', '')
            if not token:
                return HttpResponse("Ошибка авторизации.", status=403)

            try:
                response = EquipmentService.post_equipment_data(token, data)
                if response.status_code == 201:
                    return redirect('equipment_list')
                else:
                    return HttpResponse(f"Ошибка: {response.status_code} - {response.text}")
            except Exception as e:
                return HttpResponse(f"Ошибка API: {e}")
    else:
        form = EquipmentForm()

    return render(request, 'equipment/post_equipment.html', {'form': form})


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
            token = request.session.get('token', '')
            if not token:
                return HttpResponse("Ошибка авторизации.", status=403)

            try:
                response = UserEquipmentService.create_user_equipment(user_id, equipment_data, token)
                if response.status_code == 201:
                    return redirect('user_equipment')
                else:
                    return HttpResponse(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                return HttpResponse(f"Ошибка: {e}")
    else:
        form = UserEquipmentForm()

    data = UserEquipment.objects.all()

    return render(request, 'equipment/user_equipment.html', {'form': form, 'data': data})


def profile_user(request):
    try:
        token = request.session.get('token', '')
        if not token:
            return HttpResponse("Ошибка авторизации.", status=403)

        data = UserService.get_profile_data(token)
        equipment_list = [item['equipment'] for item in data]
    except RuntimeError as e:
        return HttpResponse(f"Ошибка: {e}")

    return render(request, 'authe/profile.html', {'data': equipment_list})
