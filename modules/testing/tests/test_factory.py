import pytest
from datetime import date
from modules.testing.factory import generate_user, generate_project, generate_task, generate_test_data

def test_generate_user_has_email():
    """Проверяет, что у пользователя есть email"""
    user = generate_user()
    assert "email" in user
    assert "@" in user["email"]

def test_generate_user_has_password():
    """Проверяет, что у пользователя есть пароль"""
    user = generate_user()
    assert "password" in user
    assert len(user["password"]) > 0

def test_generate_user_email_is_unique():
    """Проверяет, что каждый email уникальный"""
    user1 = generate_user()
    user2 = generate_user()
    assert user1["email"] != user2["email"]

def test_generate_user_can_override_role():
    """Проверяет, что можно переопределить роль"""
    user = generate_user(role="admin")
    assert user["role"] == "admin"

def test_generate_project_has_name():
    """Проверяет, что у проекта есть имя"""
    project = generate_project()
    assert "name" in project
    assert len(project["name"]) > 0

def test_generate_project_default_status_active():
    """Проверяет, что статус проекта по умолчанию active"""
    project = generate_project()
    assert project["status"] == "active"

def test_generate_task_deadline_not_in_past():
    """Проверяет, что дедлайн задачи не в прошлом"""
    task = generate_task()
    today = date.today()
    assert task["deadline"] >= today

def test_generate_task_edge_case_deadline_today():
    """Проверяет граничный случай: дедлайн сегодня"""
    task = generate_task(edge_case="deadline_today")
    today = date.today()
    assert task["deadline"] == today

def test_generate_task_default_status_new():
    """Проверяет, что статус задачи по умолчанию new"""
    task = generate_task()
    assert task["status"] == "new"

def test_generate_test_data_unknown_type():
    """Проверяет, что при неизвестном типе будет ошибка"""
    with pytest.raises(ValueError):
        generate_test_data("unknown_type")

def test_generate_test_data_user():
    """Проверяет генерацию пользователя через главную функцию"""
    data = generate_test_data("user")
    assert "email" in data

def test_generate_test_data_project():
    """Проверяет генерацию проекта через главную функцию"""
    data = generate_test_data("project")
    assert "name" in data

def test_generate_test_data_task():
    """Проверяет генерацию задачи через главную функцию"""
    data = generate_test_data("task")
    assert "title" in data