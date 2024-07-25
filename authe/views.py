import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from .forms import LogInForm, RegistrationForm
from .services import AuthService
from .validators import validate_login, validate_registration

logger = logging.getLogger(__name__)


@method_decorator(validate_login, 'dispatch')
class Login(FormView):
    template_name = 'authe/login.html'
    form_class = LogInForm
    success_url = '/profile/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        logger.info('Попытка входа пользователя - %s', username)
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            logger.info('Пользователь %s успешно авторизован', username)
            auth_login(self.request, user)

            try:
                token = AuthService.get_token(username, password)
                if token:
                    self.request.session['token'] = token
                    return redirect(self.success_url)
                else:
                    return JsonResponse({'error': 'Ошибка получения токена'}, status=500)
            except Exception:
                logger.error("Ошибка при получении токена", exc_info=True)
                return JsonResponse({'error': "Ошибка при получении токена"}, status=500)
        else:
            logger.warning('Проверьте правильность данных для %s', username)
            return JsonResponse({'error': 'Проверьте правильность данных'}, status=401)


class Logout(View):
    def get(self, request, *args, **kwargs):
        token = request.session.get('token', '')
        if AuthService.logout(token):
            auth_logout(request)
            logger.info('Вы разлогинились')
            return redirect('in')
        else:
            return JsonResponse({'error': 'Ошибка выхода'}, status=500)


@method_decorator(validate_registration, 'dispatch')
class Registration(FormView):
    template_name = 'authe/registration.html'
    form_class = RegistrationForm
    success_url = '/auth/login/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        AuthService.register(username, password1)
        if AuthService.register(username, password1):
            logger.info('Пользователь %s успешно зарегистрирован', username)
            return redirect(self.success_url)
        else:
            logger.warning('Ошибка регистрации %s', username)
            return JsonResponse({'error': 'Ошибка регистрации'}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
