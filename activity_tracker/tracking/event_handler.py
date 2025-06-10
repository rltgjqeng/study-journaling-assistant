# activity_tracker/tracking/event_handler.py

from utils.io_utils import save_screenshot
from utils.time_utils import get_timestamp
from utils.window_utils import get_active_window_title
from utils.id_utils import generate_prefixed_uuid
from db.manager import save_candidate_event

def handle_event_trigger():
    """이벤트 감지 시 호출: 스크린샷 저장 + 메타데이터 DB 기록"""
    timestamp = get_timestamp() 
    event_id = generate_prefixed_uuid("event")
    screenshot_path = f"./snapshots/{event_id}.png"

    save_screenshot(screenshot_path)

    event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "source": get_active_window_title(),
        "screenshot_path": screenshot_path
    }

    save_candidate_event(event)
    print(f"[이벤트 저장 완료] {event_id}")