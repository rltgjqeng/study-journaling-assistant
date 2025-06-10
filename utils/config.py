import os
import json

# config.json의 절대 경로 계산 (이 파일 기준으로 상위 디렉토리)
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))

# 전역 config 딕셔너리
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except Exception as e:
    print(f"[ERROR] config.json 로딩 실패: {e}")
    CONFIG = {}

def get(key: str, default=None):
    """
    config.json에서 설정값을 가져옵니다.
    key: str - 키 이름 (예: "tesseract_path")
    default: 기본값
    """
    return CONFIG.get(key, default)
