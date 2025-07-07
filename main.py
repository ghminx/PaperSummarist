from utils.pdf_loader import load_pdf
from model.chain import Chain, run_chain
from model.question import summary_questions
from utils.config import Config
from hwp.run_hwp import MakeRes


docs = load_pdf('./sample/test.pdf')


# 1. Chain 인스턴스 생성 및 체인 초기화
chain_manager = Chain(model_name='gpt-4o-mini', api_key=Config.OPENAI_API_KEY)
chain = chain_manager.create_chain()

# 2. 문서 처리 
print("🔹 전체 문서 요약 처리 중...")
section_summaries = {}
for key, question in summary_questions.items():
    print(f"🔎 {key} 처리 중...")
    section_summaries[key] = run_chain(chain, question, docs)

# 3. 한글 생성 및 저장 
hwp = MakeRes(frame_path='./hwp/frame.hwp', sav_path='./hwp/res.hwpx', res=section_summaries)
hwp.run()
