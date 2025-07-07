import streamlit as st
from utils.pdf_loader import load_pdf
from model.chain import Chain, run_chain
from model.question import summary_questions
from utils.config import Config
from hwp.run_hwp import MakeResST
import tempfile

# 기본 설정
st.set_page_config(page_title="논문 요약기")
st.title("📄 논문 요약기")

# 파일 업로드
uploaded_file = st.file_uploader("논문 PDF 파일을 업로드하세요", type=["pdf"])

# 1. Chain 인스턴스 생성 및 체인 초기화
chain_manager = Chain(model_name='gpt-4o-mini', api_key=Config.OPENAI_API_KEY)
chain = chain_manager.create_chain()


if st.button('요약 실행'):

    with st.spinner('논문을 읽고 요약 중입니다....'):
        
        # 1. 업로드된 PDF를 임시파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name  # 파일 경로

        # 2. 파일 경로 기반으로 PDF 텍스트 로드
        docs = load_pdf(tmp_path)
        
        print("🔹 전체 문서 요약 처리 중...")
        section_summaries = {}
        for key, question in summary_questions.items():
            print(f"🔎 {key} 처리 중...")
            section_summaries[key] = run_chain(chain, question, docs)

        st.success("✅ 요약 완료!")
        
        # 한글 
        hwp_maker = MakeResST(frame_path="./hwp/frame.hwp", res=section_summaries)
        hwpx_path = hwp_maker.run_and_return_file()

        # 임시폴더(Temp)에 저장된 파일을 읽음 
        with open(hwpx_path, "rb") as f:
            hwpx_data = f.read()

        st.download_button(
            label="📥 한글 파일 다운로드 (.hwpx)",
            data=hwpx_data,
            file_name="논문요약.hwpx",
            mime="application/hancom.hwpx"
        )
        
        
with open('./hwp/frame.hwp', "rb") as f:
    hwpx_data = f.read()