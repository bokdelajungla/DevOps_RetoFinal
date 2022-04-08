import base64
from typing import Dict

from flask import request

from server import create_app
from endpoints.public import login_user
from endpoints.private import token_required
from flask import request, jsonify, make_response, current_app
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import jwt
import uuid
import datetime
from sqlalchemy.sql import func


def log_testUser():
    with create_app().test_client() as test_client:
        '''
        Si se utiliza el esquema de la autenticación "Basic", las credenciales son construidas de esta forma:
            - El usuario y la contraseña se combinan con dos puntos (aladdin:opensesame).
            - El string resultante está basado en la codificación base64 (YWxhZGRpbjpvcGVuc2VzYW1l).
        '''
        message = "testUser:testPass"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        path = 'https://127.0.0.1:12345/login'
        headers = {'Authorization': 'Base ' + base64_message}
        response = test_client.get(path=path, headers=headers)

        return response


def test_almacena_post_no_token():
    # Create a test client using the Flask application configured for testing
    with create_app().test_client() as test_client:
        response = test_client.post('/almacena?string=main')
        assert response.status_code == 403
        assert b"token is missing" in response.data


def test_almacena_post_no_token():
    # Create a test client using the Flask application configured for testing
    with create_app().test_client() as test_client:
        response = log_testUser()
        test_request = 'https://127.0.0.1:12345/almacena?string=main'
        test_request.headers.add('X-Service-Token', response.headers.get('X-Service-Token'))
        response = test_client.post(test_request)
        assert response.status_code == 200
        assert b"main ADDED" in response.data

def test_almacena_bad_request_no_string_parameter():
    # Create a test client using the Flask application configured for testing
    with create_app().test_client() as test_client:
        response = test_client.post('/almacena?bad=main')
        assert response.status_code == 403
        assert b"token is missing" in response.data
    return 0

def test_almacena_get():
    # Create a test client using the Flask application configured for testing
    with create_app().test_client() as test_client:
        response = test_client.get('/almacena?string=main')
        assert response.status_code == 405
    return 0
