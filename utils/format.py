import re 

# 개조식 텍스트 포맷팅 함수
def format_bullet_text(text):
    # 항목들 추출
    items = re.findall(r"- ([^:]+):\s?([^-\n]+)", text)
    if not items:
        return text  # 개조식이 아니면 그대로 반환
    # 항목들을 공백 세 칸으로 연결
    return "###".join([f"-{key.strip()}: {value.strip()}" for key, value in items])

