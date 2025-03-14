# filepath: c:\Users\HISTEREOGENIK\Documents\DEV-PROJECTS\DS-TECHTEST\full-stack-user-crud\tests\conftest.py
import pytest
from server.app import create_app
from server.db import users_collection

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "pass123",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
        "active": True
    }

@pytest.fixture
def created_user(client, user_data):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.get_json()

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clean up the database before each test
    users_collection.delete_many({})
    yield
    # Clean up the database after each test
    users_collection.delete_many({})