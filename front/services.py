import logging

import requests

logger = logging.getLogger(__name__)


class EquipmentService:

    @staticmethod
    def get_equipment_data(token):
        headers = {'Authorization': f'Token {token}'}
        equipment_url = 'http://127.0.0.1:8000/api/equipment/'
        response = requests.get(equipment_url, headers=headers)
        logger.info('Данные оборудования получены')
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post_equipment_data(token, data):
        equipment_url = 'http://127.0.0.1:8000/api/equipment/'
        headers = {'Authorization': f'Token {token}'}
        response = requests.post(equipment_url, data=data, headers=headers)
        logger.info('Данные оборудования отправлены')
        response.raise_for_status()
        return response


class UserEquipmentService:
    @staticmethod
    def create_user_equipment(user_id, equipment_data, token):
        api_url = 'http://127.0.0.1:8000/api/user/equipment/'
        headers = {'Authorization': f'Token {token}'}
        data = {'user': user_id, 'equipment': equipment_data}
        response = requests.post(api_url, json=data, headers=headers)
        logger.info('Данные оборудования отправлены')
        response.raise_for_status()
        return response


class UserService():
    @staticmethod
    def get_profile_data(token):
        api_url = 'http://127.0.0.1:8000/api/profile/'
        headers = {'Authorization': f'Token {token}'}

        try:
            response = requests.get(api_url, headers=headers)
            logger.info('Данные профиля получены')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Ошибка: {e}")
