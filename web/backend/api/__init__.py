# web/backend/api/__init__.py
from flask import Blueprint

# 질문 관련 API 블루프린트
from .questions import questions_bp
# 질문 후보 관련 API 블루프린트
from .candidates import candidates_bp

# API 블루프린트 등록
def create_api(app):
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(candidates_bp, url_prefix='/api/question_candidates')
