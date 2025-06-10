-- 질문 테이블 (question.db에 사용)
CREATE TABLE IF NOT EXISTS question (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    highlight TEXT NOT NULL,
    memo TEXT DEFAULT '',
    source TEXT NOT NULL
);

-- 이벤트 후보 테이블 (candidate_event.db에 사용)
CREATE TABLE IF NOT EXISTS candidate_event (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    screenshot_path TEXT NOT NULL
);


-- OCR 처리 전 fragment 정보 저장
CREATE TABLE IF NOT EXISTS fragment_record (
    event_id TEXT NOT NULL,
    frag_id TEXT NOT NULL,
    bbox TEXT NOT NULL,
    type TEXT NOT NULL,
    ocr_text TEXT DEFAULT NULL,
    PRIMARY KEY (event_id, frag_id)
);

-- OCR 최종 조합 결과 저장
CREATE TABLE IF NOT EXISTS event_textblock (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    source TEXT,
    full_text TEXT,
    fragments_json TEXT
);

-- LLM 기반 질문 후보 테이블
CREATE TABLE IF NOT EXISTS question_candidate (
    id               TEXT PRIMARY KEY,
    event_id         TEXT NOT NULL,
    timestamp        TEXT NOT NULL,
    source           TEXT NOT NULL,
    question_text    TEXT NOT NULL,
    confirmed        INTEGER DEFAULT 0,
    candidate_index  INTEGER NOT NULL DEFAULT 0,
    is_selected      INTEGER NOT NULL DEFAULT 0
);
