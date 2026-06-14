import pytest
from app import create_app
from db import db
from modules.testing.crud import *
from modules.testing.models import TestSuite, TestResult

@pytest.fixture
def app_context():
    """Создаёт временную базу данных для тестов"""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # временная БД
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_create_suite(app_context):
    """Тест создания набора тестов"""
    suite = create_suite("Тестовый набор", "Описание")
    assert suite.id is not None
    assert suite.name == "Тестовый набор"
    assert suite.description == "Описание"

def test_get_all_suites(app_context):
    """Тест получения всех наборов"""
    create_suite("Набор 1")
    create_suite("Набор 2")
    suites = get_all_suites()
    assert len(suites) == 2

def test_get_suite(app_context):
    """Тест получения набора по ID"""
    suite = create_suite("Набор для поиска")
    found = get_suite(suite.id)
    assert found is not None
    assert found.name == "Набор для поиска"

def test_update_suite(app_context):
    """Тест обновления набора"""
    suite = create_suite("Старое имя")
    update_suite(suite.id, name="Новое имя")
    updated = get_suite(suite.id)
    assert updated.name == "Новое имя"

def test_delete_suite(app_context):
    """Тест удаления набора"""
    suite = create_suite("Набор для удаления")
    suite_id = suite.id
    delete_suite(suite_id)
    deleted = get_suite(suite_id)
    assert deleted is None

def test_add_result(app_context):
    """Тест добавления результата"""
    suite = create_suite("Набор с результатами")
    result = add_result(suite.id, "auth_module", "pass", 100)
    assert result.id is not None
    assert result.status == "pass"
    assert result.duration_ms == 100

def test_get_results_by_suite(app_context):
    """Тест получения всех результатов для набора"""
    suite = create_suite("Набор для результатов")
    add_result(suite.id, "mod1", "pass", 10)
    add_result(suite.id, "mod2", "fail", 20)
    results = get_results_by_suite(suite.id)
    assert len(results) == 2