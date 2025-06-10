import requests
import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # local_client/의 부모 디렉토리 (즉 root/)
DB_DIR = os.path.join(BASE_DIR, 'db')


# Flask API 서버 URL (받아들이는 엔드포인트)
question_api_url = "http://localhost:5001/api/questions/store_data"
candidate_api_url = "http://localhost:5001/api/question_candidates/store_data"


# DB 연결 함수
def get_db_connection(db_path):
    """DB 연결 함수 (SQLite)"""
    db_path = os.path.join(DB_DIR, db_path)   # 위에서 지정된 경로에 따라 db wjqrms.
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 데이터를 딕셔너리 형식으로 반환
    return conn

# 데이터 조회 함수 (question.db)
def get_data_from_question_db():
    """question.db에서 데이터 가져오기"""
    conn = get_db_connection('question.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM question')  # 'question' 테이블에서 데이터 조회
    rows = cursor.fetchall()  # 모든 데이터 반환
    conn.close()
    return [dict(row) for row in rows]  # 결과를 딕셔너리 형식으로 반환

# 데이터 조회 함수 (question_candidate.db)
def get_data_from_candidates_db():
    """question_candidate.db에서 데이터 가져오기"""
    conn = get_db_connection('question_candidate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM question_candidate')  # 'question_candidate' 테이블에서 데이터 조회
    rows = cursor.fetchall()  # 모든 데이터 반환
    conn.close()
    return [dict(row) for row in rows]  # 결과를 딕셔너리 형식으로 반환

# 데이터를 Flask 서버로 전송
def send_to_flask(data, api_url):
    """받은 데이터를 지정된 Flask API로 전송"""
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴
        print("서버에 데이터 전송 완료!")
    except requests.exceptions.RequestException as e:
        print(f"서버 전송 오류: {e}")

# 실제 로직 (main() 없애고, 서브프로세스에서 호출 가능하게 변경)
def process_and_send_data():
    """DB에서 데이터를 가져와서 Flask 서버로 전송"""
    # question.db와 question_candidate.db에서 데이터 가져오기
    question_data = get_data_from_question_db()
    candidate_data = get_data_from_candidates_db()

    # 데이터를 서버에 전송
    if question_data:
        send_to_flask(question_data, question_api_url)  # question.db 데이터를 서버로 전송
    else:
        print("question.db에 저장된 데이터가 없습니다.")
    
    if candidate_data:
        send_to_flask(candidate_data, candidate_api_url)  # question_candidate.db 데이터를 서버로 전송
    else:
        print("question_candidate.db에 저장된 데이터가 없습니다.")

#for test
if __name__ == "__main__":
    process_and_send_data()
