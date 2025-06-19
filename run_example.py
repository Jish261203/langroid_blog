from agents.coordinator_agent import CoordinatorAgent
from langroid.language_models.openai_gpt import OpenAIGPT, OpenAIGPTConfig
from dotenv import load_dotenv
import json

load_dotenv()

def extract_keyword(question: str) -> str:
    llm = OpenAIGPT(OpenAIGPTConfig())
    prompt = f"""
From the blog question below, suggest a 2–5 word SEO target keyword.

Question: "{question}"

Just return the keyword.
"""
    response = llm.generate(prompt, max_tokens=10)
    return response.message.strip().strip('"')

if __name__ == "__main__":
    question = input("Enter your blog topic/question: ")
    target_kw = extract_keyword(question)
    print(f"\n[Using target keyword: {target_kw}]\n")
    agent = CoordinatorAgent()
    result = agent.answer(question, target_kw)
    print(json.dumps(result, indent=2, ensure_ascii=False))
