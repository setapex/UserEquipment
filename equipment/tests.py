from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from .models import Equipment, UserEquipment


class EquipmentAPIListTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()
        self.client.login(username='admin', password='adminpass')
        self.equipment_data = {
            'name': 'New Equipment',
            'inventory_number': 789,
            'nomenclature_number': 101
        }
        self.url = '/api/equipment/'

    def test_create_equipment(self):
        response = self.client.post(self.url, self.equipment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().name, 'New Equipment')

    def test_get_equipment_list(self):
        Equipment.objects.create(**self.equipment_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'New Equipment')


class UserEquipmentAPIListTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()
        self.client.login(username='admin', password='adminpass')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.equipment = Equipment.objects.create(
            name="Test Equipment",
            inventory_number=123,
            nomenclature_number=456
        )
        self.user_equipment_data = {
            'user': self.user.id,
            'equipment': {
                'name': 'New Equipment',
                'inventory_number': 789,
                'nomenclature_number': 101
            }
        }
        self.url = '/api/user/equipment/'

    def test_create_user_equipment(self):
        response = self.client.post(self.url, self.user_equipment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserEquipment.objects.count(), 1)
        self.assertEqual(UserEquipment.objects.get().equipment.name, 'New Equipment')

    def test_get_user_equipment_list(self):
        UserEquipment.objects.create(user=self.user, equipment=self.equipment)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['equipment']['name'], 'Test Equipment')


class ProfileUserAPIListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.equipment = Equipment.objects.create(
            name="Test Equipment",
            inventory_number=123,
            nomenclature_number=456
        )
        self.user_equipment = UserEquipment.objects.create(user=self.user, equipment=self.equipment)
        self.url = '/api/profile/'

    def test_get_profile_user_equipment_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['equipment']['name'], 'Test Equipment')
