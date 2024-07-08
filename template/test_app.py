import pytest
from app import app, inject_foo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    context = app.app_context()
    context.push()
    client = app.test_client()
    yield client
    context.pop()


def test_inject_foo():
    foo = inject_foo()
    assert foo['foo'] == 'I am foo.'


def test_index(client):
    response = client.get('/')
    data = response.get_data(as_text=True)
    assert 'hello flask' in data


def test_watchlist(client):
    response = client.get('/watchlist')
    data = response.get_data(as_text=True)
    assert 'Return' in data
    assert 'zxb\'s Watchlist' in data
    assert response.status_code == 200


