import logging

import requests

logger = logging.getLogger(__name__)

URL = 'http://localhost:8000/auth/'


class HeadersService:
    @staticmethod
    def get_headers(token):
        return {'Authorization': f'Token {token}'}


class AuthService(HeadersService):
    @staticmethod
    def get_token(username, password):
        token_url = f'{URL}token/login'
        user_data = {
            'username': username,
            'password': password
        }
        logger.info('Попытка получения токена для %s', username)
        response = requests.post(token_url, json=user_data)
        if response.status_code == 200:
            logger.info('Токен для %s успешно получен', username)
            return response.json().get('auth_token', None)
        else:
            logger.warning('Ошибка получения токена для %s', username)
            return None

    @staticmethod
    def logout(token):
        logout_url = f'{URL}token/logout/'
        headers = HeadersService.get_headers(token)
        logger.info('Попытка выхода из аккаунта')
        response = requests.post(logout_url, headers=headers)
        return response.status_code == 204

    @staticmethod
    def register(username, password):
        registration_url = f'{URL}api/auth/users/'
        data = {
            'username': username,
            'password': password,
        }
        logger.info('Попытка регистрации пользователя - %s', username)
        response = requests.post(registration_url, data=data)
        return response
