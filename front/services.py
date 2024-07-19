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
            logger.info('Данные оборудования получены')
            return response.json()
        else:
            logger.error(f"Ошибка получения данных оборудования")
            return JsonResponse({"error": "Ошибка получения данных оборудования"}, status=response.status_code)

    @staticmethod
    def post_equipment_data(token, data):
        equipment_url = f'{URL}equipment/'
        headers = HeadersService.get_headers(token)
        response = requests.post(equipment_url, data=data, headers=headers)
        if response.status_code in [200, 201]:
            logger.info('Данные оборудования отправлены')
            return response
        else:
            logger.error(f"Ошибка отправки данных оборудования")
            return JsonResponse({"error": "Ошибка отправки данных оборудования"}, status=response.status_code)


class UserEquipmentService(HeadersService):
    @staticmethod
    def create_user_equipment(user_id, equipment_data, token):
        api_url = f'{URL}user/equipment/'
        headers = HeadersService.get_headers(token)
        data = {'user': user_id, 'equipment': equipment_data}
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code in [200, 201]:
            logger.info('Данные оборудования отправлены')
            return response
        else:
            logger.error(f"Ошибка отправки данных пользователя")
            return JsonResponse({"error": "Ошибка отправки данных пользователя"}, status=response.status_code)


class UserService(HeadersService):
    @staticmethod
    def get_profile_data(token):
        api_url = f'{URL}profile/'
        headers = HeadersService.get_headers(token)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            logger.info('Данные профиля получены')
            return response.json()
        else:
            logger.error(f"Ошибка получения данных профиля")
            return JsonResponse({"error": "Ошибка получения данных профиля"}, status=response.status_code)
