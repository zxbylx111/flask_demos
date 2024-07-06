import pytest
from app import app
from flask import url_for, session


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    app.secret_key = 'secret string'
    client = app.test_client()
    app_ctx = app.app_context()
    app_ctx.push()
    yield client
    app_ctx.pop()

def test_app_exists():
    assert app is not None


def test_hello(client):
    response = client.get('/hello')
    data = response.get_data(as_text=True)
    assert 'Hello, Human!' in data
    assert '[Not Authenticated]' in data

    response = client.get('/set/xin')
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith('name='):
            cookie_value = cookie.split(';')[0].split('=')[1]
            response = client.get('/hello')
            data = response.get_data(as_text=True)
            assert 'Hello, %s!' % cookie_value in data
            assert '[Not Authenticated]' in data
            break
    # 测试带session的情况
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    response = client.get('/hello')
    data = response.get_data(as_text=True)
    assert '[Not Authenticated]' not in data
    assert '[Authenticated]' in data


def test_go_back(client):
    response = client.get('/goback/12')
    data = response.get_data(as_text=True)
    assert 'Welcome to 2012!' in data

    response = client.get('/goback/hong')
    assert response.status_code == 404


def test_hi(client):
    response = client.get('/hi')
    assert response.status_code == 302


def test_404(client):
    response = client.get('/404')
    assert response.status_code == 404


def test_foo(client):
    response = client.get('/foo')
    data = response.get_json()
    assert data['name'] == 'zxb'
    assert data['gender'] == 'male'
    assert response.status_code == 200


def test_json_error(client):
    response = client.get('/json_error')
    data = response.get_json()
    assert data['message'] == 'Error!'
    assert response.status_code == 500


def test_set_cookie(client):
    response = client.get('/set/zhao')
    assert response.status_code == 302
    assert response.location in url_for('hello')
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if cookie.startswith('name='):
            cookie_value = cookie.split(';')[0].split('=')[1]
            assert cookie_value == 'zhao'
            break


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 302
    assert response.location in url_for('hello')


def test_admin(client):
    response = client.get('/admin')
    assert response.status_code == 403
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    response = client.get('/admin')
    data = response.get_data(as_text=True)
    assert response.status_code == 200
    assert 'Welcome to admin page.' in data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    response = client.get('/logout')
    assert 'logged_in' not in sess
    assert response.status_code == 302
