from typing import List
from agents.query_agent import Hit
from langroid.language_models.openai_gpt import OpenAIGPT, OpenAIGPTConfig
from dotenv import load_dotenv

load_dotenv()

class SummarizerAgent:
    def __init__(self):
        self.llm = OpenAIGPT(OpenAIGPTConfig())

    def summarize(self, hits: List[Hit]) -> str:
        context = "\n".join([f"{hit.title}: {hit.snippet}" for hit in hits])
        prompt = f"Summarize the following search results into a 2–3 sentence blog summary:\n\n{context}"
        response = self.llm.generate(prompt, max_tokens=120)
        return response.message.strip()
