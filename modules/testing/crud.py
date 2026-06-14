from db import db
from .models import TestSuite, TestResult

def create_suite(name, description=""):
    """Создать новый набор тестов"""
    suite = TestSuite(name=name, description=description)
    db.session.add(suite)
    db.session.commit()
    return suite

def get_all_suites():
    """Получить все наборы"""
    return TestSuite.query.all()

def get_suite(suite_id):
    return db.session.get(TestSuite, suite_id)

def update_suite(suite_id, name=None, description=None):
    """Обновить набор"""
    suite = get_suite(suite_id)
    if name:
        suite.name = name
    if description:
        suite.description = description
    db.session.commit()
    return suite

def delete_suite(suite_id):
    """Удалить набор"""
    suite = get_suite(suite_id)
    db.session.delete(suite)
    db.session.commit()

def add_result(suite_id, module_name, status, duration_ms):
    """Добавить результат теста"""
    result = TestResult(
        suite_id=suite_id,
        module_name=module_name,
        status=status,
        duration_ms=duration_ms
    )
    db.session.add(result)
    db.session.commit()
    return result

def get_results_by_suite(suite_id):
    """Получить все результаты для набора"""
    return TestResult.query.filter_by(suite_id=suite_id).all()