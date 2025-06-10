import sqlite3
import os
import json
from collections import defaultdict
from datetime import datetime

# 서버 DB 경로
BASE_DIR = os.path.dirname(__file__)  # db/manager.py 위치 기준
DB_DIR = BASE_DIR
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")
DB_PATH_QUESTION = os.path.join(DB_DIR, "question.db")
DB_PATH_CANDIDATE = os.path.join(DB_DIR, "question_candidate.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()

    for db_path in [DB_PATH_QUESTION, DB_PATH_CANDIDATE]:
        with sqlite3.connect(db_path) as conn:
            conn.executescript(schema)

def get_db_connection(db_path):
    """DB 연결 함수 (SQLite)"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 데이터를 딕셔너리 형식으로 반환
    return conn

# 서버 DB에 질문 저장
def save_web_question(entry: dict):
    with sqlite3.connect(DB_PATH_QUESTION) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO question (id, timestamp, highlight, memo, source)
            VALUES (?, ?, ?, ?, ?)
        """, (
            entry["id"], entry["timestamp"], entry["highlight"], entry.get("memo", ""), entry["source"]
        ))

# 서버 DB에 질문 후보 저장 (candidate_index, is_selected 추가)
def save_web_question_candidate(candidate: dict):
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO question_candidate (id, event_id, timestamp, source, question_text, confirmed, candidate_index, is_selected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate["id"], candidate["event_id"], candidate["timestamp"], candidate["source"],
            candidate["question_text"], candidate["confirmed"], candidate["candidate_index"], candidate["is_selected"]
        ))

# 서버 DB에서 모든 질문 조회
def get_all_web_questions():
    with sqlite3.connect(DB_PATH_QUESTION) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM question')
        rows = cur.fetchall()
    return [dict(zip(["id", "timestamp", "highlight", "memo", "source"], row)) for row in rows]

# 서버 DB에서 모든 질문 후보 조회 (candidate_index, is_selected 포함)
def get_all_web_question_candidates():
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM question_candidate')
        rows = cur.fetchall()
    return [dict(zip(["id", "event_id", "timestamp", "source", "question_text", "confirmed", "candidate_index", "is_selected"], row)) for row in rows]

# 타임라인(날짜->소스->시각)순의 계층적 정렬을 위한 조회 함수
def get_questions_grouped_by_date_and_source():
    with sqlite3.connect(DB_PATH_QUESTION) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, timestamp, highlight, memo, source
            FROM question
            ORDER BY DATE(timestamp) DESC, source ASC, timestamp ASC
        """)
        rows = cur.fetchall()

    result = defaultdict(lambda: defaultdict(list))

    for row in rows:
        q = dict(zip(["id", "timestamp", "highlight", "memo", "source"], row))
        date_key = q["timestamp"][:10]  # YYYY-MM-DD 추출
        result[date_key][q["source"]].append(q)

    return result  # { '2025-05-31': { 'Notion': [..], 'YouTube': [..] }, ... }

def get_candidates_grouped_by_date_and_source():
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, event_id, timestamp, source, question_text, confirmed, candidate_index, is_selected
            FROM question_candidate
            ORDER BY DATE(timestamp) DESC, source ASC, timestamp ASC
        """)
        rows = cur.fetchall()

    result = defaultdict(lambda: defaultdict(list))

    for row in rows:
        c = dict(zip(["id", "event_id", "timestamp", "source", "question_text", "confirmed", "candidate_index", "is_selected"], row))
        date_key = c["timestamp"][:10]
        result[date_key][c["source"]].append(c)

    return result

# 확정된 candidate question.db로 재라벨링하는 함수
def confirm_question_candidate(candidate_id: str):
    # 1. 후보 데이터 조회
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, timestamp, source, question_text, candidate_index, is_selected
            FROM question_candidate
            WHERE id = ?
        """, (candidate_id,))
        row = cur.fetchone()

    if not row:
        return False  # 없는 ID일 경우 처리

    question_entry = {
        "id": row[0],
        "timestamp": row[1],
        "highlight": row[3],
        "memo": "",  # 후보에는 memo 없으므로 빈 문자열로
        "source": row[2],
    }

    # 2. question.db에 삽입
    save_web_question(question_entry)

    # 3. 후보 DB에서 삭제
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM question_candidate WHERE id = ?", (candidate_id,))
        conn.commit()

    return True

# confirm deny당한 question_candidate 삭제
def deny_question_candidate(candidate_id: str):
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM question_candidate WHERE id = ?", (candidate_id,))
        conn.commit()
