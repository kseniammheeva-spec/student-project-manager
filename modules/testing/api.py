import logging
from flask import Blueprint, request, jsonify
from .factory import generate_test_data
from .crud import create_suite, add_result, get_all_suites, get_results_by_suite

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаём Blueprint (это как маленькое приложение внутри большого)
testing_bp = Blueprint('testing', __name__, url_prefix='/api/tests')


@testing_bp.route('/hello', methods=['GET'])
def hello_test():
    """Простая проверка, что модуль работает"""
    return jsonify({
        "message": "Testing module is alive!", 
        "status": "ok"
    })


@testing_bp.route('/generate', methods=['POST'])
def generate():
    """Генерирует тестовые данные (пользователь, проект, задача)"""
    data = request.get_json()
    
    # Логируем запрос для отладки
    logging.info(f"Получен запрос на генерацию: {data}")
    
    # Проверяем, что данные прислали
    if not data:
        return jsonify({
            "error": True, 
            "message": "Нет данных. Отправь JSON с полем entity_type"
        }), 400
    
    # Получаем тип сущности
    entity_type = data.get('entity_type')
    
    # Проверяем, что тип указан
    if not entity_type:
        return jsonify({
            "error": True, 
            "message": "Укажи entity_type: user, project или task"
        }), 400
    
    # Получаем переопределения (если есть)
    overrides = data.get('overrides', {})
    
    try:
        # Генерируем тестовые данные
        result = generate_test_data(entity_type, **overrides)
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "error": True, 
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "error": True, 
            "message": f"Неожиданная ошибка: {str(e)}"
        }), 500


@testing_bp.route('/run', methods=['POST'])
def run_tests():
    """Запускает тесты и сохраняет результаты в БД"""
    data = request.get_json() or {}
    suite_name = data.get('suite_name', 'Demo Run')
    
    # Создаём новый набор тестов
    suite = create_suite(suite_name, "Автоматический прогон тестов")
    
    # Имитируем запуск тестов (здесь потом добавишь реальные тесты)
    add_result(suite.id, "auth_module", "pass", 123)
    add_result(suite.id, "projects_module", "pass", 45)
    add_result(suite.id, "tasks_module", "fail", 67)
    
    # Считаем статистику
    results = get_results_by_suite(suite.id)
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    
    return jsonify({
        "suite_id": suite.id,
        "suite_name": suite.name,
        "status": "completed",
        "passed": passed,
        "failed": failed,
        "total": passed + failed
    })


@testing_bp.route('/results', methods=['GET'])
def get_results():
    """Получить все наборы тестов"""
    suites = get_all_suites()
    result = []
    for suite in suites:
        result.append({
            "id": suite.id,
            "name": suite.name,
            "description": suite.description,
            "created_at": str(suite.created_at),
            "results_count": len(suite.results) if hasattr(suite, 'results') else 0
        })
    return jsonify(result)


@testing_bp.route('/results/<int:suite_id>', methods=['GET'])
def get_suite_results(suite_id):
    """Получить результаты конкретного набора тестов"""
    results = get_results_by_suite(suite_id)
    if not results:
        return jsonify({
            "error": True,
            "message": f"Набор с id={suite_id} не найден или нет результатов"
        }), 404
    
    result_list = []
    for r in results:
        result_list.append({
            "id": r.id,
            "module_name": r.module_name,
            "status": r.status,
            "duration_ms": r.duration_ms,
            "run_at": str(r.run_at)
        })
    
    return jsonify({
        "suite_id": suite_id,
        "results": result_list
    })