from langchain_openai import ChatOpenAI
from utils.config import Config
from langchain_core.output_parsers import StrOutputParser
from model.prompts import prompt

class Chain:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key
        self.llm = self._initialize_model()

    def _initialize_model(self):
        return ChatOpenAI(model_name=self.model_name, api_key=self.api_key)

    def create_chain(self):
        return prompt | self.llm | StrOutputParser()


def run_chain(chain, question, context):
    return chain.invoke({
        "question": question,
        "context": context
    })