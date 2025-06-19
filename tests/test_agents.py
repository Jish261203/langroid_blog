import pytest
from agents.coordinator_agent import CoordinatorAgent
from agents.query_agent import QueryAgent, Hit
from agents.summarizer_agent import SummarizerAgent
from agents.seo_agent import SEOAgent, SEOResult
from agents.blog_agent import BlogAgent

def sample_question():
    return "How can wearable technology improve chronic disease management?"

def test_query_agent():
    agent = QueryAgent()
    hits = agent.search(sample_question())
    assert isinstance(hits, list)
    assert len(hits) > 0
    for hit in hits:
        assert isinstance(hit, Hit)
        assert isinstance(hit.title, str) and hit.title.strip()
        assert isinstance(hit.snippet, str) and hit.snippet.strip()

def test_summarizer_agent():
    query_agent = QueryAgent()
    hits = query_agent.search(sample_question())
    agent = SummarizerAgent()
    summary = agent.summarize(hits)
    assert isinstance(summary, str)
    assert len(summary.split()) > 10

def test_seo_agent():
    summarizer = SummarizerAgent()
    query_agent = QueryAgent()
    hits = query_agent.search(sample_question())
    summary = summarizer.summarize(hits)
    target_kw = "wearable technology"
    agent = SEOAgent()
    seo = agent.optimize(summary, target_kw)
    assert isinstance(seo, SEOResult)
    assert isinstance(seo.title, str) and seo.title.strip() and len(seo.title) <= 60
    assert isinstance(seo.meta_description, str) and seo.meta_description.strip() and len(seo.meta_description) <= 160
    assert isinstance(seo.keywords, list) and len(seo.keywords) >= 1
    assert isinstance(seo.h1, str) and seo.h1.strip()
    assert target_kw.lower() in seo.title.lower()
    assert target_kw.lower() in seo.meta_description.lower()
    assert target_kw.lower() in seo.h1.lower()

def test_blog_agent():
    summarizer = SummarizerAgent()
    query_agent = QueryAgent()
    hits = query_agent.search(sample_question())
    summary = summarizer.summarize(hits)
    target_kw = "wearable technology"
    seo_agent = SEOAgent()
    seo = seo_agent.optimize(summary, target_kw)
    agent = BlogAgent()
    blog = agent.write_blog(summary, seo)
    assert isinstance(blog, str)
    assert len(blog.split()) >= 300
    assert blog.lower().count(target_kw) >= 2
    assert seo.h1 in blog
    assert blog.startswith("#")

def test_coordinator_agent():
    agent = CoordinatorAgent()
    target_kw = "wearable technology"
    result = agent.answer(sample_question(), target_kw)
    assert isinstance(result, dict)
    assert "summary" in result and isinstance(result["summary"], str)
    assert "seo" in result and isinstance(result["seo"], dict)
    assert "blog_post" in result and isinstance(result["blog_post"], str)
    seo = result["seo"]
    assert "title" in seo and len(seo["title"]) <= 60
    assert "meta_description" in seo and len(seo["meta_description"]) <= 160
    assert "keywords" in seo and isinstance(seo["keywords"], list)
    assert "h1" in seo
    assert result["blog_post"].count(seo["keywords"][0]) >= 2
    assert len(result["blog_post"].split()) >= 300
