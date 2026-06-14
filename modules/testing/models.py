from datetime import datetime
from db import db  # импортируем db из отдельного файла

class TestSuite(db.Model):
    __tablename__ = "test_suites"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
class TestResult(db.Model):
    __tablename__ = "test_results"
    id = db.Column(db.Integer, primary_key=True)
    suite_id = db.Column(db.Integer, db.ForeignKey("test_suites.id"))
    module_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    duration_ms = db.Column(db.Integer, default=0)
    run_at = db.Column(db.DateTime, default=lambda: datetime.now())

    suite = db.relationship("TestSuite", backref="results")