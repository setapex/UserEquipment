import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from equipment.models import UserEquipment
from front.forms import EquipmentForm, UserEquipmentForm
from front.services import EquipmentService, UserEquipmentService, UserService
from front.validators import validate_auth

logger = logging.getLogger(__name__)


@method_decorator(validate_auth, name='dispatch')
class EquipmentTemplateView(TemplateView):
    template_name = 'equipment/equipment_list.html'

    def get(self, request, *args, **kwargs):
        token = self.request.session.get('token', '')
        try:
            data = EquipmentService.get_equipment_data(token)
            logger.info('Оборудование успешно получено')
            return render(request, self.template_name, {'data': data})
        except Exception as e:
            logger.error('Невозможно получить список оборудования', exc_info=True)
            return JsonResponse({'error': 'Ошибка получения оборудования'}, status=500)


@method_decorator(validate_auth, 'dispatch')
class EquipmentFormView(FormView):
    template_name = 'equipment/post_equipment.html'
    form_class = EquipmentForm
    success_url = '/equipment/'

    def form_valid(self, form):
        data = {
            'name': form.cleaned_data['name'],
            'inventory_number': form.cleaned_data['inventory_number'],
            'nomenclature_number': form.cleaned_data['nomenclature_number']
        }
        token = self.request.session.get('token', '')

        try:
            EquipmentService.post_equipment_data(token, data)
            logger.info('Оборудование успешно добавлено')
            return redirect(self.success_url)
        except Exception as e:
            logger.error("Ошибка при отправке данных", exc_info=True)
            return JsonResponse({'error': "Ошибка при отправке данных"}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


@method_decorator(validate_auth, 'dispatch')
class UserEquipmentFormView(FormView):
    template_name = 'equipment/user_equipment.html'
    form_class = UserEquipmentForm
    success_url = '/equipment/pair/'

    def form_valid(self, form):
        user_id = form.cleaned_data['user'].id
        equipment_data = {
            'name': form.cleaned_data['name'],
            'inventory_number': form.cleaned_data['inventory_number'],
            'nomenclature_number': form.cleaned_data['nomenclature_number']
        }
        token = self.request.session.get('token', '')

        try:
            UserEquipmentService.create_user_equipment(user_id, equipment_data, token)
            logger.info('Оборудование успешно добавлено')
            return redirect(self.success_url)
        except Exception as e:
            logger.critical(f"Ошибка при отправке данных: {e}")
            return JsonResponse({'error': "Ошибка при отправке данных"}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = UserEquipment.objects.all()
        return context


@method_decorator(validate_auth, 'dispatch')
class ProfileTemplateView(TemplateView):
    template_name = 'authe/profile.html'

    def get(self, request, *args, **kwargs):
        token = self.request.session.get('token', '')
        try:
            data = UserService.get_profile_data(token)
            equipment_list = [item['equipment'] for item in data]
            logger.info('Профиль успешно отображен')
        except RuntimeError as e:
            logger.error("Ошибка при получении данных профиля", exc_info=True)
            return JsonResponse({'error': "Ошибка при получении данных профиля"}, status=500)
        return render(request, self.template_name, {'data': equipment_list})
