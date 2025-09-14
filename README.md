## 🔠 논문 요약 자동화 프로그램

> 📚 논문 PDF 파일을 입력하면, 주요 내용을 **LLM 기반**으로 분석하고 미리 지정된 HWP 양식에 맞추어 **자동으로 보고서를 생성**하는 Python 기반 프로그램.

---

### 📌 주요 기능

* **LLM**을 이용한 논문 요약 처리
* 서지정보, 연구대상, 분석방법 등 주요 항목 자동 추출
* 한글(HWPX) 문서 자동 생성 및 저장
* `langchain`, `pywin32` 등 라이브러리 활용

---

### 🛠️ 실행 환경

* Python >= 3.10
* Windows OS (HWP 프리뷰 필요)
* 설치 라이브러리:

  * `openai`
  * `pandas`
  * `langchain`
  * `pywin32`

* pip install -r requirements.txt 을 통한 설치 
---

### 🚀 실행 방법

#### ▶ CLI 실행 (main.py)

```bash
python main.py
```

* `sample/test.pdf`에 있는 논문을 읽고
* 사전에 정의된 질문(`summary_questions`)으로 내용을 요약
* `hwp/frame.hwp` 템플릿에 데이터를 삽입
* 최종 `.hwpx` 형식의 한글 문서를 생성

#### ▶ 웹 인터페이스 실행 (app.py)

```bash
streamlit run app.py
```

* Streamlit 기반 웹 앱 제공
* 사용자가 브라우저에서 논문 업로드 및 요약 결과 확인 가능
* `.hwpx` 파일 다운로드 기능 포함

---

### 📞 처리 항목 예시

* 서지정보
* 추로 요약 (.목적, 방법, 결과, 결론)
* 연구 필요성 / 설계 / 대상 / 도구
* 윤리적 고려 / 분석 방법 / 결과 / 고차 / 시사점

질문은 `model/question.py`에서 정의 되어 있음

---

### 📅 참고 설정

`utils/config.py` 파일에 OpenAI API 키를 설정필요

```python
class Config:
    OPENAI_API_KEY = "sk-xxxx..."
```

---

