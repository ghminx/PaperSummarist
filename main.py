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


filename = 'test'
docs = load_pdf(f'./files/{filename}.pdf')
print("\n📄 문서 분석 시작")
print(f"   └ 파일명: '{filename}.pdf'\n")


# 1. Chain 인스턴스 생성 및 체인 초기화
chain_manager = Chain(model_name='gpt-4o-mini', api_key=Config.OPENAI_API_KEY)
chain = chain_manager.create_chain()

# 2. 문서 처리 
print("\n🔹 전체 문서 요약 처리 중...\n")
section_summaries = {}
for key, question in summary_questions.items():
    print(f"   🔎 {key} 처리 중...")
    section_summaries[key] = run_chain(chain, question, docs)

print("\n✅ 문서 요약 완료\n")

date = {'날짜' : datetime.now().strftime("%Y.%m.%d")}

section_summaries=date | section_summaries 

for key in section_summaries:
    section_summaries[key] = format_bullet_text(section_summaries[key])

# 3. 한글 생성 및 저장 
print("📝 한글 리포트 생성 시작...\n")

frame_path='./hwp/frame.hwp'
sav_path=f'./{filename}.hwp'
hwp = MakeRes(frame_path, sav_path, res=section_summaries)
hwp.run()

# 완료 메시지
print("🎉 한글 리포트 생성 완료")
print(f"💾 파일이 저장되었습니다 → {sav_path}\n")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📌 전체 프로세스 정상 종료 ✅")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")