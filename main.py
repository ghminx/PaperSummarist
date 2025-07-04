from utils.pdf_loader import load_pdf
from model.chain import Chain, run_chain
from model.question import raw_questions, summary_questions
from utils.config import Config
from hwp.run_hwp import MakeRes


docs = load_pdf('./sample/test.pdf')


# Chain 인스턴스 생성 및 체인 초기화
chain_manager = Chain(model_name='gpt-4o-mini', api_key=Config.OPENAI_API_KEY)
chain = chain_manager.create_chain()

# 1. 서지정보 및 초록 추출
raw_extracted = {}
for section, question in raw_questions.items():
    print(f"🔹 {section} 처리 중...")
    raw_extracted[section] = run_chain(chain, question, docs)
    

# 2. 전체 문서 요약
print("🔹 전체 문서 요약 처리 중...")
question = '이 논문 전체 내용을 간략히 요약해 주세요. 주요 목적, 방법, 결과, 결론 중심으로 정리해 주세요.'
doc_summary = run_chain(chain, question, docs)

# 3. 세부 요약 항목 추출 (요약본 기반)
section_summaries = {}
for key, question in summary_questions.items():
    print(f"🔎 {key} 처리 중...")
    section_summaries[key] = run_chain(chain, question, doc_summary)

# 4. 결과 병합
final_summary = raw_extracted | section_summaries

# 5. 결과 키 확인 (선택 사항)
print("\n✅ 최종 요약 항목 목록:")
for k in final_summary.keys():
    print(f"- {k}")
    
hwp = MakeRes('./hwp/frame.hwp', '//', final_summary)
hwp.run()


# 1차 작업완료 프롬프트 수정 필요, 2. 전체 문서 요약 삭제할지 확인


