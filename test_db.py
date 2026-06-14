from app import app, db
from modules.testing.models import TestSuite, TestResult

with app.app_context():
    # Создаём тестовый набор
    suite = TestSuite(name="My First Suite", description="Тестирование модулей")
    db.session.add(suite)
    db.session.commit()
    
    # Добавляем результат
    result = TestResult(suite_id=suite.id, module_name="auth", status="pass", duration_ms=100)
    db.session.add(result)
    db.session.commit()
    
    print("Всего наборов:", TestSuite.query.count())
    print("Всего результатов:", TestResult.query.count())