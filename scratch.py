from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import os 
from dotenv import load_dotenv


# API Key 
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# DataLoader
loader = PyMuPDFLoader('./sample/test.pdf')
docs = loader.load()

# ✅ 4. 문서 전체 내용을 하나의 문자열로 병합
full_text = "\n".join([doc.page_content for doc in docs])

# ✅ 5. 프롬프트 정의
prompt = PromptTemplate.from_template(
    """당신은 논문 문서를 분석하는 AI입니다.
아래 문서 전체 내용을 참고하여 질문에 답해주세요. 
문서에 없으면 없다고 답하세요. 답변은 한국어로 하세요.

#질문:
{question}

#문서 내용:
{context}

#답변:"""
)

llm = ChatOpenAI(model_name = 'gpt-4o-mini', api_key=OPENAI_API_KEY) 


chain = (
    prompt
    | llm
    | StrOutputParser()
)

question = """
논문에서 초록을 찾아 다음과 같이 요약 정리해주세요

- 목적 : 

- 방법 : 

- 결과 : 

- 결론 : 

"""

response = chain.stream({
    "question": question,
    "context": full_text
})

for c in response:
    print(c, end='', flush=True)










