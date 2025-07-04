from langchain_community.document_loaders import PyMuPDFLoader


# DataLoader
def load_pdf(filpath: str) -> str:
    """_summary_

    Args:
        filpath (str): PDF 파일 경로 

    Returns:
        str: PDF 내의 텍스트 
    """
    loader = PyMuPDFLoader(filpath)
    docs = loader.load()

    # 문서 전체 내용을 하나의 문자열로 병합
    return "\n".join([doc.page_content for doc in docs])
