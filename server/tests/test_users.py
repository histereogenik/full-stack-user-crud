# filepath: c:\Users\HISTEREOGENIK\Documents\DEV-PROJECTS\DS-TECHTEST\full-stack-user-crud\tests\test_users.py
import json

def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json == []

def test_create_user(client, user_data):

    response = client.post('/users/', data=json.dumps(user_data), content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['_id'] is not None
    assert data['username'] == "testuser"
    assert data['preferences']['timezone'] == "UTC"
    assert data['active'] is True
    assert "created_ts" in data

def test_get_single_user(client, created_user):
    user_id = created_user["_id"]
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == created_user["username"]

def test_update_user(client, created_user):
    user_id = created_user["_id"]
    updated_data = {
        "username": "updateduser",
        "active": False
    }

    response = client.put(f'/users/{user_id}', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "updateduser"
    assert data["active"] is False

def test_delete_user(client, created_user):
    user_id = created_user["_id"]
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json["message"] == "User deleted"

    # Confirm user no longer exists
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404