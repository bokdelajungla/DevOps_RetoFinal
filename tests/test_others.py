'''
Tests para funcionalidades de server.py
'''
from unittest import mock
import argparse

from server import create_app
from server import main
from config.default import PORT


def test_create_app():
    app = create_app()
    assert(app is not None)


def test_default_parameters():
    port = main()
    assert port == PORT


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(port=23456))
def test_parameters(mock_args):
    port = main()
    assert port == 23456


def test_homepage():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/')
    assert response.status_code == 200
    assert b"Servicio Web para Cadenas" in response.data

