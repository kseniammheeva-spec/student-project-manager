from app import app, db
from modules.testing.crud import *

with app.app_context():
    # Создаём
    suite = create_suite("Тест CRUD", "Проверяем работу")
    print("Создан:", suite.id, suite.name)
    
    # Добавляем результат
    result = add_result(suite.id, "my_module", "pass", 50)
    print("Результат добавлен:", result.status)
    
    # Получаем все
    all_suites = get_all_suites()
    print("Всего наборов:", len(all_suites))
    
    # Обновляем
    update_suite(suite.id, name="Новое имя")
    updated = get_suite(suite.id)
    print("Обновлённое имя:", updated.name)