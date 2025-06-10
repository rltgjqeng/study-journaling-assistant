# utils/id_utils.py

import uuid

def generate_uuid():
    """순수 UUID 문자열 반환"""
    return str(uuid.uuid4())

def generate_prefixed_uuid(prefix: str):
    """접두어가 포함된 UUID 생성 (예: 'event_550e8400-e29b-41d4-a716-446655440000')"""
    return f"{prefix}_{uuid.uuid4()}"
