# activity_tracker/tracking/event_tracker.py

import time
import pyautogui

from activity_tracker.tracking.event_handler import handle_event_trigger

_stop_event_tracker = False

def stop_event_tracker():
    """track_user_inactivity 루프를 멈춥니다."""
    global _stop_event_tracker
    _stop_event_tracker = True

def track_user_inactivity(threshold_seconds=10):
    print(f"🖱️ 사용자 비활성 감지 시작 (기준: {threshold_seconds}초)")
    last_position = pyautogui.position()
    inactive_time = 0

    while not _stop_event_tracker:
        current_position = pyautogui.position()

        if current_position == last_position:
            inactive_time += 1
        else:
            inactive_time = 0
            last_position = current_position

        if inactive_time >= threshold_seconds * 2:  # 0.5초 단위 체크니까 2배
            print("⚠️ 비활성 상태 감지됨 → 이벤트 트리거")
            handle_event_trigger()
            inactive_time = 0

        time.sleep(0.5)

    # 루프를 빠져나오면
    print("👋 이벤트 트래커 중단됨")