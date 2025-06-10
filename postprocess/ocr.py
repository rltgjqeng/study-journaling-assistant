# postprocess/ocr.py

import re
from PIL import Image
import pytesseract
from pix2text import Pix2Text

# Tesseract 경로 설정 (윈도우 환경)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def preprocess_image(image_path: str, max_dim: int = 1000) -> Image.Image:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    if max(w, h) > max_dim:
        if w > h:
            nw = max_dim
            nh = int(h * (max_dim / w))
        else:
            nh = max_dim
            nw = int(w * (max_dim / h))
        img = img.resize((nw, nh), Image.LANCZOS)
    return img

def run_tesseract_ocr(pil_image: Image.Image) -> str:
    try:
        return pytesseract.image_to_string(pil_image, lang='eng')
    except Exception as e:
        print(f"[OCR] Tesseract 오류: {e}")
        return ""

def run_pix2text_ocr(pil_image: Image.Image) -> list[dict]:
    try:
        p2t = Pix2Text()
        return p2t.recognize(pil_image)
    except Exception as e:
        print(f"[OCR] Pix2Text 오류: {e}")
        return []

def extract_and_merge_key_info(tess_text: str, p2t_results: list) -> str:
    """
    Tesseract와 Pix2Text 결과를 합쳐서
    --- Formulas --- (LaTeX)
    --- Text --- 형태의 문자열로 반환.
    """
    combined = {"text": "", "formulas": []}

    # 1) Tesseract 텍스트
    if tess_text.strip():
        combined["text"] += tess_text.strip() + "\n"

    # 2) Pix2Text 결과
    full = ""
    for item in p2t_results:
        if isinstance(item, str):
            full += item
        elif isinstance(item, dict):
            txt = item.get("text", "").strip()
            if item.get("type") == "text" and txt:
                full += txt
            elif item.get("type") == "formula" and txt:
                combined["formulas"].append(f"${txt}$")

    # 3) LaTeX 수식 분리
    doubles = re.findall(r"\$\$([^$]+?)\$\$", full)
    combined["formulas"] += [f"$${f.strip()}$$" for f in doubles]
    full = re.sub(r"\$\$([^$]+?)\$\$", "", full)

    singles = re.findall(r"\$([^$]+?)\$", full)
    combined["formulas"] += [f"${f.strip()}${''}" for f in singles]
    full = re.sub(r"\$([^$]+?)\$", "", full)

    # 4) 나머지 텍스트
    if full.strip():
        combined["text"] += full.strip() + "\n"

    # 5) 정리
    text_lines = [line.strip() for line in combined["text"].splitlines() if line.strip()]
    text_block = "\n".join(text_lines)
    formulas = list(dict.fromkeys(combined["formulas"]))  # 순서 보장 중복 제거

    out = ""
    if formulas:
        out += "--- Formulas ---\n" + "\n".join(formulas) + "\n\n"
    if text_block:
        out += "--- Text ---\n" + text_block

    return out
