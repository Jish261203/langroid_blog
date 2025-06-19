from agents.query_agent import QueryAgent, Hit
from agents.summarizer_agent import SummarizerAgent
from agents.seo_agent import SEOAgent, SEOResult
from agents.blog_agent import BlogAgent
from typing import Dict, Any

class CoordinatorAgent:
    def __init__(self):
        self.query_agent = QueryAgent()
        self.summarizer_agent = SummarizerAgent()
        self.seo_agent = SEOAgent()
        self.blog_agent = BlogAgent()

    def answer(self, question: str, target_kw: str) -> Dict[str, Any]:
        hits = self.query_agent.search(question)
        summary = self.summarizer_agent.summarize(hits)
        seo = self.seo_agent.optimize(summary, target_kw)
        blog = self.blog_agent.write_blog(summary, seo)
        return {
            "summary": summary,
            "seo": {
                "title": seo.title,
                "meta_description": seo.meta_description,
                "keywords": seo.keywords,
                "h1": seo.h1
            },
            "blog_post": blog
        }
