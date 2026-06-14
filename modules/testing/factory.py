"""
Модуль генерации тестовых данных.

Предоставляет функции для генерации:
- пользователей
- проектов
- задач
"""
from faker import Faker
from datetime import date, timedelta

fake = Faker()

def generate_user(**overrides):
    """Генерирует тестовые данные пользователя"""
    data = {
        "email": fake.unique.email(),
        "password": "TestPassword123!",
        "name": fake.name(),
        "role": "student"
    }
    data.update(overrides)
    return data

def generate_project(**overrides):
    """Генерирует тестовые данные проекта"""
    data = {
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=100),
        "status": "active",
        "owner_id": 1
    }
    data.update(overrides)
    return data

def generate_task(**overrides):
    """Генерирует тестовые данные задачи"""
    today = date.today()
    data = {
        "title": fake.sentence(nb_words=5),
        "description": fake.text(max_nb_chars=200),
        "deadline": today + timedelta(days=fake.random_int(1, 30)),
        "status": "new",
        "assigned_to": 1
    }
    # Граничный случай: дедлайн сегодня
    if overrides.get("edge_case") == "deadline_today":
        data["deadline"] = today
    data.update(overrides)
    return data

def generate_test_data(entity_type, **overrides):
    """Главная функция - генерирует данные нужного типа"""
    if entity_type == "user":
        return generate_user(**overrides)
    elif entity_type == "project":
        return generate_project(**overrides)
    elif entity_type == "task":
        return generate_task(**overrides)
    else:
        raise ValueError(f"Неизвестный тип: {entity_type}")