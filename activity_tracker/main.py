# root_pipelined/activity_tracker/main.py

import threading
import time
import json

import sys, os
from pynput.keyboard import GlobalHotKeys
from subprocess import run

from input_capture import start_input_capture, stop_input_capture
from tracking.event_tracker import track_user_inactivity, stop_event_tracker
from db.manager import init_db


def run_pipeline():
  script = os.path.abspath(os.path.join(__file__, '..', '..', 'postprocess', 'run_pipeline.py'))
  print(f"[RUN] postprocess/run_pipeline.py")
  run([sys.executable, script], check=True)

def run_sender():
  script = os.path.abspath(os.path.join(__file__, '..', '..', 'local_client', 'sender.py'))
  print(f"[RUN] local_client/sender.py")
  run([sys.executable, script], check=True)
  
def load_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
            return config.get("inactivity_threshold", 10)
    except Exception as e:
        print(f"[설정 불러오기 실패] 기본값 사용: {e}")
        return 10

if __name__ == "__main__":
    init_db()
    threshold = load_config()

    t_input = threading.Thread(target=start_input_capture, daemon=True)
    t_event = threading.Thread(target=lambda: track_user_inactivity(threshold), daemon=True)

    t_input.start()
    t_event.start()

    print("▶ 시스템 실행 중 — Ctrl+Shift+X 로 후처리 및 전송을 시작합니다.")

    def on_exit():
        # 1) input_capture 스레드 정리
        print("\n🛑 Ctrl+Shift+X 입력 감지 — 입력 감지 스레드 종료 중...")

        stop_input_capture()
        # 2) event_tracker 루프 정지
        stop_event_tracker()

        # 3) 후처리 및 전송
        print("🛑 후처리 및 전송 시작")
        run_pipeline()
        run_sender()

        print("[DONE] 모든 작업 완료. 프로그램을 종료합니다.")
        sys.exit(0)

    # GlobalHotKeys 컨텍스트 매니저로 블로킹 대기
    with GlobalHotKeys({
        '<ctrl>+<shift>+x': on_exit
    }) as listener:
        listener.join()