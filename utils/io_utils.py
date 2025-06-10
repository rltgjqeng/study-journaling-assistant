# utils/io_utils.py

import os
from PIL import ImageGrab

def ensure_dir(path: str):
    """지정한 디렉토리가 없으면 생성"""
    os.makedirs(path, exist_ok=True)

def save_screenshot(path: str):
    """전체 화면을 캡처해 저장 (디렉토리도 자동 생성)"""
    ensure_dir(os.path.dirname(path))
    image = ImageGrab.grab()
    image.save(path)
    print(f"[스크린샷 저장됨] {path}")
