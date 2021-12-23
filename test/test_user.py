import pytest
from app import schemas
from typing import List
# from .database import client, session
from app.config import settings
from jose import jwt


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from Rexiemedia!!!"}


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123", "firstname": "anyname",
    "lastname": "anylastname"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert new_user.firstname == "anyname"
    assert new_user.lastname == "anylastname"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('ovi@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
    

# if the route is restricted will return 401
def test_unaothorized_user_get_all_users(client):
    res = client.get(f"/users/")
    assert res.status_code == 401

# if the route is restricted will return 401
def test_unaothorized_user_get_one_users(client):
    res = client.get(f"/users/{1}")
    assert res.status_code == 401


def test_authorized_user_get(authorized_client, test_user):
    res = authorized_client.get(f"/users/{test_user['id']}")
    
    user_data = schemas.UserOut(**res.json())
    
    assert user_data.email == "hello123@gmail.com"
    assert user_data.firstname == "anyname"
    assert res.status_code == 200
    