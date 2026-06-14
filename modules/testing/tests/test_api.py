import pytest
import json
from app import create_app
from db import db

@pytest.fixture
def client():
    """Создаёт тестовый клиент для API"""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_hello_endpoint(client):
    """Тест GET /api/tests/hello"""
    response = client.get('/api/tests/hello')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "ok"

def test_generate_user_endpoint(client):
    """Тест POST /api/tests/generate для пользователя"""
    response = client.post('/api/tests/generate', 
                          json={"entity_type": "user"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "email" in data

def test_generate_project_endpoint(client):
    """Тест POST /api/tests/generate для проекта"""
    response = client.post('/api/tests/generate', 
                          json={"entity_type": "project"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "name" in data

def test_generate_task_endpoint(client):
    """Тест POST /api/tests/generate для задачи"""
    response = client.post('/api/tests/generate', 
                          json={"entity_type": "task"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "title" in data

def test_generate_invalid_type(client):
    """Тест POST /api/tests/generate с неверным типом"""
    response = client.post('/api/tests/generate', 
                          json={"entity_type": "unknown"})
    assert response.status_code == 400

def test_generate_no_data(client):
    """Тест POST /api/tests/generate без данных"""
    response = client.post('/api/tests/generate', 
                          data='',  # пустые данные
                          content_type='application/json')
    assert response.status_code == 400

def test_run_tests_endpoint(client):
    """Тест POST /api/tests/run"""
    response = client.post('/api/tests/run', 
                          json={"suite_name": "Тестовый прогон"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "suite_id" in data
    assert "passed" in data

def test_get_results_endpoint(client):
    """Тест GET /api/tests/results"""
    # Сначала создадим набор через run
    client.post('/api/tests/run', json={"suite_name": "Для просмотра"})
    
    response = client.get('/api/tests/results')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) >= 1