import logging

import requests
from django.http import JsonResponse

from authe.services import HeadersService

logger = logging.getLogger(__name__)

URL = 'http://127.0.0.1:8000/api/'


class EquipmentService(HeadersService):
    @staticmethod
    def get_equipment_data(token):
        headers = HeadersService.get_headers(token)
        equipment_url = f'{URL}equipment/'
        response = requests.get(equipment_url, headers=headers)
        if response.status_code == 200:
            logger.info('The equipment data has been received')
            return response.json()
        else:
            logger.error(f"Hardware data acquisition error")
            return JsonResponse({"error": "Hardware data acquisition error"}, status=response.status_code)

    @staticmethod
    def post_equipment_data(token, data):
        equipment_url = f'{URL}equipment/'
        headers = HeadersService.get_headers(token)
        response = requests.post(equipment_url, data=data, headers=headers)
        if response.status_code in [200, 201]:
            logger.info('The hardware data has been sent')
            return None
        else:
            logger.error(f"Error sending equipment data")
            return JsonResponse({"error": "Error sending equipment data"}, status=response.status_code)


class UserEquipmentService(HeadersService):
    @staticmethod
    def create_user_equipment(user_id, equipment_data, token):
        api_url = f'{URL}user/equipment/'
        headers = HeadersService.get_headers(token)
        data = {'user': user_id, 'equipment': equipment_data}
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code in [200, 201]:
            logger.info('The hardware data has been sent')
            return None
        else:
            logger.error(f"Error sending user data")
            return JsonResponse({"error": "Error sending user data"}, status=response.status_code)


class UserService(HeadersService):
    @staticmethod
    def get_profile_data(token):
        api_url = f'{URL}profile/'
        headers = HeadersService.get_headers(token)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            logger.info('Profile data received')
            return response.json()
        else:
            logger.error(f"Error receiving profile data")
            return []
