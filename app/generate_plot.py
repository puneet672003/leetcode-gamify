import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class PlotAgent:
    def __init__(self, model: str = "open-mistral-7b"):
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

    def generate_score_string(self, scores: dict[str, int]):
        score_string = ""
        for user, score in scores.items():
            score_string += f"Warrior: {user} Power Level: {score}. \n"

        return score_string

    def run(self, scores: dict[str, int], system_prompt: str):
        score_string = self.generate_score_string(scores)
        chain = self._build_chain(system_prompt, score_string)

        return chain.invoke({"input": score_string})
