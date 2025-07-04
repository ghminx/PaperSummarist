from langchain_core.prompts import PromptTemplate


prompt =  PromptTemplate.from_template("""당신은 논문 문서를 분석하는 AI입니다.
아래 문서 전체 내용을 참고하여 질문에 답해주세요. 
문서에 없으면 없다고 답하세요. 답변은 한국어로 하세요.

#질문:
{question}

#문서 내용:
{context}

#답변:
"""
)   
        
        
