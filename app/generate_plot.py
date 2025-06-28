import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class PlotAgent:
    def __init__(self, api_key: str = None, model: str = "open-mistral-7b"):
        API_KEY = os.environ["MISTRAL_API_KEY"]
        if API_KEY is None:
            raise ValueError("Missing Mistral AI API Key.")

        self.model = model
        self.llm = ChatMistralAI(api_key=API_KEY, model_name=self.model)

    def _build_chain(self, system_prompt: str, user_prompt: str):
        prompt = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("human", "{input}")]
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain

    def run(self, user_input: str, system_prompt: str = "You are a helpful assistant."):
        chain = self._build_chain(system_prompt, user_input)
        return chain.invoke({"input": user_input})
