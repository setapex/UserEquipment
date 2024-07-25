import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from equipment.models import UserEquipment
from front.forms import EquipmentForm, UserEquipmentForm
from front.services import EquipmentService, UserEquipmentService, UserService


logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class EquipmentTemplateView(TemplateView):
    template_name = 'equipment/equipment_list.html'

    def get(self, request, *args, **kwargs):
        token = self.request.session.get('token', '')
        try:
            data = EquipmentService.get_equipment_data(token)
            logger.info('The equipment has been successfully received')
            return render(request, self.template_name, {'data': data})
        except Exception:
            logger.error('It is not possible to get a list of equipment', exc_info=True)
            return JsonResponse({'error': 'Error getting the equipment'}, status=500)

@method_decorator(login_required, 'dispatch')
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
            logger.info('The equipment has been added successfully')
            return redirect(self.success_url)
        except Exception:
            logger.error("Error when sending data", exc_info=True)
            return JsonResponse({'error': "Error when sending data"}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


@method_decorator(login_required, 'dispatch')
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
            logger.info('The equipment has been added successfully')
            return redirect(self.success_url)
        except Exception:
            logger.error(f"Error when sending data", exc_info=True)
            return JsonResponse({'error': "Error when sending data"}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = UserEquipment.objects.all()
        return context


@method_decorator(login_required, 'dispatch')
class ProfileTemplateView(TemplateView):
    template_name = 'authe/profile.html'

    def get(self, request, *args, **kwargs):
        token = self.request.session.get('token', '')
        try:
            data = UserService.get_profile_data(token)
            if not data:
                logger.error("No profile data received")
                return render(request, self.template_name, {'error': "No profile data available"})
            equipment_list = [item['equipment'] for item in data]
            logger.info('The profile has been successfully displayed')
            return render(request, self.template_name, {'data': equipment_list})
        except Exception as e:
            logger.error("Error receiving profile data", exc_info=True)
            return render(request, self.template_name, {'error': "Error receiving profile data"})
