"""
Pytest configuration and shared fixtures.
"""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config.config import TestingConfig
from app.db.connection import MongoDBConnection


@pytest.fixture(scope="module")
def app():
    app: Flask = create_app(app_config=TestingConfig)
    with app.app_context():

        yield app


@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="module")
def db(app: Flask):
    mongo_conn = MongoDBConnection.get_instance()
    mongo_conn.init_connection()
    yield mongo_conn.db

    # Clean up the database after tests
    mongo_conn.db.client.drop_database(app.config["DB_NAME"])
