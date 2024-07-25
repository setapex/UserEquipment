from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from authe.services import AuthService

class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('in')
        self.username = 'testuser'
        self.password = 'qwertyzxc'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    @patch.object(AuthService, 'get_token')
    def test_login_success(self, mock_get_token):
        mock_get_token.return_value = 'token'

        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/profile/')
        self.assertEqual(self.client.session.get('token'), 'token')

    @patch.object(AuthService, 'get_token')
    def test_login_error_token(self, mock_get_token):
        mock_get_token.return_value = None

        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Ошибка получения токена'})

    @patch.object(AuthService, 'get_token')
    def test_login_error(self, mock_get_token):
        mock_get_token.return_value = 'token'
        response = self.client.post(self.login_url, {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Проверьте правильность данных'})
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')


class LogoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('out')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.session['token'] = 'token'

    @patch.object(AuthService, 'logout')
    def test_logout_success(self, mock_logout):
        mock_logout.return_value = True

        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('in'))
        self.assertNotIn('_auth_user_id', self.client.session)

    @patch.object(AuthService, 'logout')
    def test_logout_error(self, mock_logout):
        mock_logout.return_value = False

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Ошибка выхода'})


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.registration_url = reverse('reg')

    @patch.object(AuthService, 'register')
    def test_registration_success(self, mock_register):
        mock_register.return_value = True
        response = self.client.post(self.registration_url, {
            'username': 'testuser',
            'password1': 'qwertyzxc',
            'password2': 'qwertyzxc'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('in'))

    @patch.object(AuthService, 'register')
    def test_registration_error(self, mock_register):
        mock_register.return_value = False
        response = self.client.post(self.registration_url, {
            'username': 'testuser',
            'password1': 'testu',
            'password2': 'test'
        })
        self.assertEqual(response.status_code, 400)