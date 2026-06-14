from flask import Flask
from db import db  # импортируем db из отдельного файла

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Подключаем db к app
    db.init_app(app)
    
    # Импортируем модели ПОСЛЕ инициализации db
    from modules.testing.models import TestSuite, TestResult
    
    # Регистрируем API
    from modules.testing.api import testing_bp
    app.register_blueprint(testing_bp)
    
    @app.route('/')
    def hello():
        return 'Testing module is running! Go to /api/tests/hello'
    
    return app

# Создаём приложение
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ База данных создана!")
    app.run(debug=True)