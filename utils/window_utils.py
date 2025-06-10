# utils/window_utils.py

import pyautogui

def get_active_window_title():
    """현재 포커스된 창의 제목 반환, 실패 시 'Unknown'"""
    try:
        win = pyautogui.getActiveWindow()
        return win.title if win else "Unknown"
    except:
        return "Unknown"
