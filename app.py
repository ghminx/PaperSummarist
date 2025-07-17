import streamlit as st
from utils.pdf_loader import load_pdf
from utils.format import format_bullet_text
from model.chain import Chain, run_chain
from model.question import summary_questions
from utils.config import Config
from hwp.run_hwp import MakeResST
import tempfile
from datetime import datetime
import os 

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
        
        status_placeholder = st.empty()
        
        section_summaries = {}
        progress = st.progress(0)
        status_placeholder = st.empty()

        for i, (key, q) in enumerate(summary_questions.items(), 1):
            status_placeholder.text(f"🔎 {key} 처리 중...")
            progress.progress(i / len(summary_questions))
            section_summaries[key] = run_chain(chain, q, docs)

        # 프로그래스바, 텍스트 삭제
        progress.empty()
        status_placeholder.empty()
        
        date = {'날짜' : datetime.now().strftime("%Y.%m.%d")}

        section_summaries=date | section_summaries 

        for key in section_summaries:
            section_summaries[key] = format_bullet_text(section_summaries[key])

        st.success("✅ 요약 완료!")
        
        # 한글 
        hwp_maker = MakeResST(frame_path="./hwp/frame.hwp", res=section_summaries)
        hwpx_path = hwp_maker.run_and_return_file()

        # 임시폴더(Temp)에 저장된 파일을 읽음 
        with open(hwpx_path, "rb") as f:
            hwpx_data = f.read()
            
        file_basename = os.path.splitext(uploaded_file.name)[0]
        file_name_for_download = f"{file_basename}_요약.hwp"

        st.download_button(
            label="📥 한글 파일 다운로드 (.hwp)",
            data=hwpx_data,
            file_name=file_name_for_download,
            mime="application/hancom.hwp"
        )
        
        
