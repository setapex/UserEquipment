from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from front.forms import EquipmentForm, UserEquipmentForm


class EquipmentTemplateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    @patch('front.services.EquipmentService.get_equipment_data')
    def test_get_equipment_success(self, mock_get_equipment_data):
        mock_get_equipment_data.return_value = []
        response = self.client.get(reverse('equipment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_list.html')
        self.assertIn('data', response.context)

    @patch('front.services.EquipmentService.get_equipment_data')
    def test_get_equipment_error(self, mock_get_equipment_data):
        mock_get_equipment_data.side_effect = Exception('Error')
        response = self.client.get(reverse('equipment_list'))
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Error getting the equipment'})


class EquipmentFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_get_form(self):
        response = self.client.get(reverse('post_equipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/post_equipment.html')
        self.assertIsInstance(response.context['form'], EquipmentForm)

    @patch('front.services.EquipmentService.post_equipment_data')
    def test_post_form_invalid(self, mock_post_equipment_data):
        mock_post_equipment_data.side_effect = Exception('Error')
        data = {
            'name': 'Test Equipment',
            'inventory_number': '12345',
            'nomenclature_number': '54321'
        }
        response = self.client.post(reverse('post_equipment'), data)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Error when sending data'})


class UserEquipmentFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_get_form(self):
        response = self.client.get(reverse('user_equipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/user_equipment.html')
        self.assertIsInstance(response.context['form'], UserEquipmentForm)
        self.assertIn('data', response.context)

    @patch('front.services.UserEquipmentService.create_user_equipment')
    def test_post_form_valid(self, mock_create_user_equipment):
        data = {
            'user': self.user.id,
            'name': 'User Equipment',
            'inventory_number': '12345',
            'nomenclature_number': '54321'
        }
        response = self.client.post(reverse('user_equipment'), data)
        self.assertRedirects(response, reverse('user_equipment'))
        mock_create_user_equipment.assert_called_once()

    @patch('front.services.UserEquipmentService.create_user_equipment')
    def test_post_form_invalid(self, mock_create_user_equipment):
        mock_create_user_equipment.side_effect = Exception('Error')
        data = {
            'user': self.user.id,
            'name': 'User Equipment',
            'inventory_number': '12345',
            'nomenclature_number': '54321'
        }
        response = self.client.post(reverse('user_equipment'), data)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Error when sending data'})


class ProfileTemplateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    @patch('front.services.UserService.get_profile_data')
    def test_get_profile_success(self, mock_get_profile_data):
        mock_get_profile_data.return_value = [{'equipment': 'Test Equipment'}]
        response = self.client.get(reverse('profile_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authe/profile.html')
        self.assertIn('data', response.context)

    @patch('front.services.UserService.get_profile_data')
    def test_get_profile_error(self, mock_get_profile_data):
        mock_get_profile_data.side_effect = Exception('Error')
        response = self.client.get(reverse('profile_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authe/profile.html')
        self.assertIn('error', response.context)
