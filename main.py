from utils.pdf_loader import load_pdf
from model.chain import Chain, run_chain
from model.question import summary_questions
from utils.config import Config
from hwp.run_hwp import MakeRes
from datetime import datetime
import re

# 개조식 텍스트 포맷팅 함수
def format_bullet_text(text):
    # 항목들 추출
    items = re.findall(r"- ([^:]+):\s?([^-\n]+)", text)
    if not items:
        return text  # 개조식이 아니면 그대로 반환
    # 항목들을 공백 세 칸으로 연결
    return "###".join([f"-{key.strip()}: {value.strip()}" for key, value in items])



docs = load_pdf('./files/test.pdf')

# 1. Chain 인스턴스 생성 및 체인 초기화
chain_manager = Chain(model_name='gpt-4o-mini', api_key=Config.OPENAI_API_KEY)
chain = chain_manager.create_chain()

# 2. 문서 처리 
print("🔹 전체 문서 요약 처리 중...")
section_summaries = {}
for key, question in summary_questions.items():
    print(f"🔎 {key} 처리 중...")
    section_summaries[key] = run_chain(chain, question, docs)


date = {'날짜' : datetime.now().strftime("%Y.%m.%d")}

section_summaries=date | section_summaries 

for key in section_summaries:
    section_summaries[key] = format_bullet_text(section_summaries[key])

# 3. 한글 생성 및 저장 
hwp = MakeRes(frame_path='./hwp/frame.hwp', sav_path='./hwp/res.hwp', res=section_summaries)
hwp.run()
