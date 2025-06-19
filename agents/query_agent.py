from dataclasses import dataclass
from typing import List
from langroid.language_models.openai_gpt import OpenAIGPT, OpenAIGPTConfig
import json
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Hit:
    title: str
    snippet: str

class QueryAgent:
    def __init__(self):
        self.llm = OpenAIGPT(OpenAIGPTConfig())

    def search(self, question: str) -> List[Hit]:
        prompt = f"""
Generate 3 realistic search engine results for the query below.
Each should have a 'title' and 'snippet' summarizing the result.
Respond ONLY in JSON array of objects: [{{"title": "...", "snippet": "..."}}]

Query: "{question}"
"""
        response = self.llm.generate(prompt, max_tokens=300)
        msg = response.message.strip()
        if msg.startswith("```"):
            msg = msg.split('\n', 1)[-1].rsplit("```", 1)[0].strip()
        results = json.loads(msg)
        return [Hit(**r) for r in results]