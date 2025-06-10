# postprocess/llm.py
import re
import ollama

OLLAMA_MODEL_NAME = "gemma3:4b"

def generate_questions_with_llm(key_info: str, model_name: str = OLLAMA_MODEL_NAME) -> str:
    prompt = f"""
You are an AI assistant specialized in generating student-like questions from textbook excerpts in screenshots. 
Below is the extracted core information from the textbook. Based on this information, generate 3–5 questions a student might naturally ask while reading the material.

**Only generate questions based on the provided information; do not make up details that are not present.**
Your questions should focus on key concepts, definitions, formulas, or help the reader gain a deeper understanding of the topic. Also, please consider any potential OCR errors or incomplete formatting in the text and reconstruct the meaning logically to generate meaningful questions.

**1. Generate questions based on the following:**
   - Questions related to important definitions or rules
   - Questions that encourage a deeper understanding of concepts or formulas
   - Questions that address confusion or uncertainty that a student might have on their first reading

**2. The questions should be in the following format:**
   Q1: ...
   Q2: ...
   Q3: ...

--- Extracted Core Information ---
{key_info}
---
Generated Questions:

Please make sure to only generate 3 questions based on the provided information. Do not generate more than three.
Generate exactly 3 questions. Do not generate more or fewer than three.
"""
    try:
        resp = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",   "content": "질문을 생성해 주세요."}
            ]
        )
        return resp["message"]["content"]
    except Exception as e:
        print(f"[LLM] 오류: {e}")
        return ""

def parse_questions(llm_output: str) -> list[str]:
    """
    '1. 질문1', '2) 질문2' 같은 번호 매김을 제거하고
    순수 텍스트 질문 리스트로 반환.
    """
    lines = [l.strip() for l in llm_output.splitlines() if l.strip()]
    parsed = []
    for line in lines:
        # 앞 숫자+점 또는 괄호 제거
        q = re.sub(r'^\d+[\.\)]\s*', '', line)
        parsed.append(q)
    return parsed
