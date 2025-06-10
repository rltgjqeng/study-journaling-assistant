# utils/time_utils.py

from datetime import datetime

def get_timestamp():
    """현재 시간을 'YYYYMMDD_HHMMSS' 포맷 문자열로 반환"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_precise_timestamp():
    """ms 단위까지 포함된 타임스탬프 ('YYYYMMDD_HHMMSS_fff')"""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
