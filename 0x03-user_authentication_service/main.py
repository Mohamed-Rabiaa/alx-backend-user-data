#!/usr/bin/env python3
"""
Main file
"""
import requests

HOME_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    register_user
    """
    response1 = requests.post('{}/users'.format(HOME_URL), data={
        'email': email, 'password': password})
    assert response1.status_code == 200
    assert response1.json() == {'email': "guillaume@holberton.io",
                                "message": "user created"}

    response2 = requests.post('{}/users'.format(HOME_URL), data={
        'email': email, 'password': password})
    assert response2.status_code == 400
    assert response2.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    log_in_wrong_password
    """
    response = requests.post('{}/sessions'.format(HOME_URL), data={
        'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    log_in
    """
    response = requests.post('{}/sessions'.format(HOME_URL), data={
        'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    profile_unlogged
    """
    response = requests.get('{}/profile'.format(HOME_URL), cookies={
        'session_id': None})
    assert response.status_code == 403

    response = requests.get('{}/profile'.format(HOME_URL), cookies={
        'session_id': 'Fake_session_id'})
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    profile_logged
    """
    response = requests.get('{}/profile'.format(HOME_URL), cookies={
        'session_id': session_id})
    assert response.status_code == 200
    assert 'email' in response.json()


def log_out(session_id: str) -> None:
    """
    log_out
    """
    response1 = requests.delete('{}/sessions'.format(HOME_URL), cookies={
        'session_id': session_id})
    assert response1.status_code == 200
    assert response1.json() == {"message": "Bienvenue"}

    response2 = requests.delete('{}/sessions'.format(HOME_URL), cookies={
        'session_id': session_id})
    assert response2.status_code == 403


def reset_password_token(email: str) -> str:
    """
    reset_password_token
    """
    response = requests.post('{}/reset_password'.format(HOME_URL), data={
        'email': email})
    assert response.status_code == 200
    assert 'email' in response.json()
    assert response.json().get('email') == email
    assert 'reset_token' in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    update_password
    """
    response = requests.put('{}/reset_password'.format(HOME_URL), data={
        'email': email, 'reset_token': reset_token,
        'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
