import pytest
from app.main import app
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post('/shorten', json={'original_url': 'https://www.example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data
    assert data['short_url'].startswith('http')

def test_shorten_url_invalid_input(client):
    response = client.post('/shorten', json={'url': 'invalid.com'})
    assert response.status_code == 400 or response.status_code == 422  
    data = response.get_json()
    assert 'error' in data

def test_redirect_from_short_url(client):
    
    post_response = client.post('/shorten', json={'original_url': 'https://www.google.com'})
    short_url = post_response.get_json()['short_url']
    short_path = short_url.split('/')[-1]

    
    redirect_response = client.get(f'/{short_path}')
    assert redirect_response.status_code == 302  
    assert 'https://www.google.com' in redirect_response.headers['Location']

def test_url_statistics(client):
    post_response = client.post('/shorten', json={'original_url': 'https://www.github.com'})
    short_url = post_response.get_json()['short_url']
    short_path = short_url.split('/')[-1]

    client.get(f'/{short_path}')

    stats_response = client.get(f'/stats/{short_path}')
    assert stats_response.status_code == 200
    data = stats_response.get_json()
    assert data['original_url'] == 'https://www.github.com'
    assert isinstance(data['clicks'], int)
    assert data['clicks'] >= 1
