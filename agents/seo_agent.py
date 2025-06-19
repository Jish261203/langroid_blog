from dataclasses import dataclass
from typing import List
from langroid.language_models.openai_gpt import OpenAIGPT, OpenAIGPTConfig
from dotenv import load_dotenv
import json

load_dotenv()

@dataclass
class SEOResult:
    title: str
    meta_description: str
    keywords: List[str]
    h1: str

class SEOAgent:
    def __init__(self):
        self.llm = OpenAIGPT(OpenAIGPTConfig())

    def optimize(self, summary: str, target_kw: str) -> SEOResult:
        prompt = f"""
From the following blog summary and target keyword, generate SEO data:
- SEO Title (≤ 60 chars, includes keyword)
- Meta Description (≤ 160 chars, includes keyword)
- 3 focus keywords (comma-separated, includes target keyword)
- H1 heading (includes keyword)

Respond in JSON:
{{
"title": "...",
"meta_description": "...",
"keywords": "...",
"h1": "..."
}}

Summary: {summary}
Target Keyword: {target_kw}
"""
        response = self.llm.generate(prompt, max_tokens=180)
        msg = response.message.strip()
        if msg.startswith("```"):
            msg = msg.split('\n', 1)[-1].rsplit("```", 1)[0].strip()
        data = json.loads(msg)
        keywords = [kw.strip() for kw in data["keywords"].split(",")]
        return SEOResult(data["title"], data["meta_description"], keywords, data["h1"])
