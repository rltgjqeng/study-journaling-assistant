import os
import json
from db.manager import load_candidate_events_after, save_question_candidates
from postprocess.ocr import (
    preprocess_image,
    run_tesseract_ocr,
    run_pix2text_ocr,
    extract_and_merge_key_info
)
from postprocess.llm import (
    generate_questions_with_llm,
    parse_questions
)

# --- 설정 ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATE_FILE = "postprocess/state.json" #os.path.join(PROJECT_ROOT, 'state.json')

# --- 상태 관리 ---
def load_state() -> dict:
    """
    상태 파일을 로드합니다. 없으면 초기화된 상태를 반환합니다.
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_timestamp": ""}  # 처음에는 빈 값으로 설정

def save_state(state: dict):
    """
    상태 파일을 저장합니다.
    """
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# --- 메인 파이프라인 ---
def run_pipeline():
    state = load_state()
    last_ts = state.get('last_timestamp', "")
    
    # `last_timestamp`가 비어 있으면, 모든 이벤트를 로드하도록 설정
    if not last_ts:
        print("[INFO] 첫 번째 실행이므로 모든 이벤트를 로드합니다.")
        last_ts = "1900-01-01 00:00:00"  # 매우 오래된 날짜로 설정

    events = load_candidate_events_after(last_ts)

    if not events:
        print("[INFO] 새로운 이벤트가 없습니다.")
        return

    candidates = []
    for ev in events:
        eid = ev['event_id']
        ts = ev['timestamp']
        src = ev['source']
        img_path = ev['screenshot_path']

        print(f"[PROCESS] {eid} - OCR 및 질문 생성 시작")
        # 1️⃣ 이미지 전처리
        img = preprocess_image(img_path)

        # 2️⃣ OCR
        tess_text = run_tesseract_ocr(img)
        p2t_res = run_pix2text_ocr(img)

        # 3️⃣ 핵심 정보 추출
        key_info = extract_and_merge_key_info(tess_text, p2t_res)
        if not key_info.strip():
            print(f"[WARN] {eid} - 핵심 정보 부족으로 건너뜀")
            continue

        # 4️⃣ LLM 질문 생성
        llm_out = generate_questions_with_llm(key_info)
        questions = parse_questions(llm_out)

        # 5️⃣ 후보 리스트 구성
        for idx, q in enumerate(questions):
            candidates.append({
                'id': f"{eid}_{idx}",  # 고유 ID 생성
                'event_id': eid,
                'timestamp': ts,
                'source': src,
                'question_text': q,
                'confirmed': 0,  # 초기값: 미확인
                'candidate_index': idx,
                'is_selected': 0  # 초기값: 선택 안됨
            })

    # 6️⃣ DB 저장 및 상태 업데이트
    if candidates:
        save_question_candidates(candidates)
        new_ts = events[-1]['timestamp']  # 마지막 이벤트의 타임스탬프
        state['last_timestamp'] = new_ts
        save_state(state)
        print(f"[DONE] {len(candidates)}개의 질문 후보 저장, 상태 업데이트 완료.")
    else:
        print("[INFO] 생성된 질문 후보가 없습니다.")

if __name__ == '__main__':
    run_pipeline()
