import sqlite3
import os
import json

DB_DIR = "db"
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

DB_PATH_QUESTION = os.path.join(DB_DIR, "question.db")
DB_PATH_EVENT = os.path.join(DB_DIR, "candidate_event.db")
DB_PATH_TEXTBLOCK = os.path.join(DB_DIR, "event_textblock.db")
DB_PATH_CANDIDATE = os.path.join(DB_DIR, "question_candidate.db")
DB_PATH_FRAGMENT = os.path.join(DB_DIR, "fragment_record.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()

    for db_path in [DB_PATH_QUESTION, DB_PATH_EVENT, DB_PATH_TEXTBLOCK, DB_PATH_CANDIDATE, DB_PATH_FRAGMENT]:
        with sqlite3.connect(db_path) as conn:
            conn.executescript(schema)

# -------------------------------
# ✅ 질문 저장: question.db
# -------------------------------

def save_question(entry: dict):
    with sqlite3.connect(DB_PATH_QUESTION) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO question (id, timestamp, highlight, memo, source)
            VALUES (?, ?, ?, ?, ?)
        """, (
            entry["id"], entry["timestamp"], entry["highlight"], entry.get("memo", ""), entry["source"]
        ))

# -------------------------------
# ✅ 이벤트 저장: candidate_event.db
# -------------------------------

def save_candidate_event(event: dict):
    with sqlite3.connect(DB_PATH_EVENT) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO candidate_event (event_id, timestamp, source, screenshot_path)
            VALUES (?, ?, ?, ?)
        """, (
            event["event_id"], event["timestamp"], event["source"], event["screenshot_path"]
        ))

def load_candidate_events_after(timestamp: str) -> list[dict]:
    with sqlite3.connect(DB_PATH_EVENT) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT event_id, timestamp, source, screenshot_path
            FROM candidate_event
            WHERE timestamp > ?
            ORDER BY timestamp ASC
        """, (timestamp,))
        rows = cur.fetchall()
    return [dict(zip(["event_id", "timestamp", "source", "screenshot_path"], row)) for row in rows]

# -------------------------------
# ✅ Fragment 저장: fragment_record.db
# -------------------------------

def save_fragment(fragment: dict):
    with sqlite3.connect(DB_PATH_FRAGMENT) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO fragment_record (event_id, frag_id, bbox, type)
            VALUES (?, ?, ?, ?)
        """, (
            fragment["event_id"], fragment["frag_id"], json.dumps(fragment["bbox"]), fragment["type"]
        ))

def update_ocr_text(event_id: str, frag_id: str, ocr_text: str):
    with sqlite3.connect(DB_PATH_FRAGMENT) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE fragment_record
            SET ocr_text = ?
            WHERE event_id = ? AND frag_id = ?
        """, (ocr_text, event_id, frag_id))

# -------------------------------
# ✅ 텍스트블록 저장: event_textblock.db
# -------------------------------

def save_textblock_with_fragments(entry: dict):
    with sqlite3.connect(DB_PATH_TEXTBLOCK) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO event_textblock (
                event_id, timestamp, source,
                full_text, fragments_json
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            entry["event_id"], entry["timestamp"], entry["source"],
            entry["full_text"], entry["fragments_json"]
        ))

# -------------------------------
# ✅ 질문 후보 저장: question_candidate.db
# -------------------------------

def save_question_candidate(candidate: dict):
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO question_candidate (
                id, event_id, timestamp, source,
                question_text, confirmed, candidate_index, is_selected
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate["id"], candidate["event_id"], candidate["timestamp"],
            candidate["source"], candidate["question_text"], candidate.get("confirmed", 0),
            candidate.get("candidate_index", 0), candidate.get("is_selected", 0)
        ))

def save_question_candidates(candidates: list[dict]):
    with sqlite3.connect(DB_PATH_CANDIDATE) as conn:
        cur = conn.cursor()
        cur.executemany("""
            INSERT INTO question_candidate (
                id, event_id, timestamp, source,
                question_text, confirmed, candidate_index, is_selected
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                c["id"], c["event_id"], c["timestamp"],
                c["source"], c["question_text"], c.get("confirmed", 0),
                c.get("candidate_index", 0), c.get("is_selected", 0)
            ) for c in candidates
        ])
