from flask import Blueprint, request, jsonify
from web.backend.db.manager import (
    save_web_question_candidate,
    get_all_web_question_candidates,
    confirm_question_candidate,
    deny_question_candidate,
    get_candidates_grouped_by_date_and_source
)

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route("/", methods=["GET"])
def get_candidates():
    """DB에서 질문 후보 데이터를 조회"""
    candidates = get_all_web_question_candidates()  # 서버 DB에서 모든 후보 데이터 가져오기
    return jsonify(candidates)

@candidates_bp.route("/store_data", methods=["POST"])
def store_candidates():
    """POST 요청으로 받은 질문 후보 데이터를 DB에 저장"""
    data = request.get_json()
    if data:
        for candidate in data:
            # candidate_index와 is_selected가 없으면 기본값을 설정
            candidate['candidate_index'] = candidate.get('candidate_index', 0)
            candidate['is_selected'] = candidate.get('is_selected', 0)
            save_web_question_candidate(candidate)  # DB에 저장
        return jsonify({"message": "질문 후보 데이터가 저장되었습니다."}), 200
    return jsonify({"message": "잘못된 요청"}), 400

# 정렬된 질문 후보 데이터 조회
@candidates_bp.route("/grouped", methods=["GET"])
def get_grouped_candidates():
    """정렬된 질문 후보 데이터를 조회"""
    grouped_data = get_candidates_grouped_by_date_and_source()
    return jsonify(grouped_data)

# ✅ 후보 → 질문으로 이동 (confirm)
@candidates_bp.route("/confirm/<candidate_id>", methods=["POST"])
def confirm_candidate(candidate_id):
    """질문 후보를 확정된 질문으로 이동"""
    success = confirm_question_candidate(candidate_id)
    if success:
        return jsonify({"message": f"{candidate_id} 확인 완료"}), 200
    else:
        return jsonify({"message": "존재하지 않는 후보 ID"}), 404

# ✅ 후보 삭제 (deny)
@candidates_bp.route("/deny/<candidate_id>", methods=["POST"])
def deny_candidate(candidate_id):
    """질문 후보를 삭제"""
    deny_question_candidate(candidate_id)
    return jsonify({"message": f"{candidate_id} 삭제 완료"}), 200
