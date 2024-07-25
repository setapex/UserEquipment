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
        logger.info('An attempt to get a token for %s', username)
        response = requests.post(token_url, json=user_data)
        if response.status_code == 200:
            logger.info('The token for %s has been successfully received', username)
            return response.json().get('auth_token', None)
        else:
            logger.warning('Error getting the token for %s', username)
            return None

    @staticmethod
    def logout(token):
        logout_url = f'{URL}token/logout/'
        headers = HeadersService.get_headers(token)
        logger.info('Attempt to log out of the account')
        response = requests.post(logout_url, headers=headers)
        return response.status_code == 204

    @staticmethod
    def register(username, password):
        registration_url = f'{URL}api/auth/users/'
        data = {
            'username': username,
            'password': password,
        }
        logger.info('Attempt to register account - %s', username)
        requests.post(registration_url, data=data)
        return True
