from agents.seo_agent import SEOResult
from langroid.language_models.openai_gpt import OpenAIGPT, OpenAIGPTConfig
from dotenv import load_dotenv

load_dotenv()

class BlogAgent:
    def __init__(self):
        self.llm = OpenAIGPT(OpenAIGPTConfig())

    def write_blog(self, summary: str, seo: SEOResult) -> str:
        prompt = f"""
Write a 300–500 word blog post using the SEO info and summary below.
- Start with the H1
- Use at least 2 H2 subheadings
- Paragraphs ≤ 4 lines
- Use the target keyword at least 2 times, and sprinkle the other keywords
- Output in Markdown

Summary: {summary}
H1: {seo.h1}
Title: {seo.title}
Meta Description: {seo.meta_description}
Keywords: {', '.join(seo.keywords)}
"""
        response = self.llm.generate(prompt, max_tokens=700)
        return response.message.strip()
