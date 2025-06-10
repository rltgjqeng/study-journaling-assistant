# web/backend/api/questions.py
from flask import Blueprint, request, jsonify
from web.backend.db.manager import save_web_question, get_all_web_questions, get_questions_grouped_by_date_and_source

questions_bp = Blueprint('questions', __name__)

@questions_bp.route("/store_data", methods=["POST"])
def store_question():
    """POST 요청으로 받은 질문 데이터를 DB에 저장"""
    data = request.get_json()
    
    if data:
        for question in data:
            save_web_question(question)
        return jsonify({"message": "질문 데이터가 저장되었습니다."}), 200
    return jsonify({"message": "잘못된 데이터!"}), 400

@questions_bp.route("/", methods=["GET"])
def get_questions():
    """DB에서 질문 데이터를 조회"""
    questions = get_all_web_questions()  # 서버 DB에서 모든 질문 데이터 가져오기
    return jsonify(questions)

# ✅ 새로운 grouped API
@questions_bp.route("/grouped", methods=["GET"])
def get_grouped_questions():
    grouped_data = get_questions_grouped_by_date_and_source()
    return jsonify(grouped_data)