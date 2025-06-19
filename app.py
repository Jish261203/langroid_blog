# app.py
import streamlit as st
from agents.coordinator_agent import CoordinatorAgent
from run_example import extract_keyword

st.set_page_config(page_title="AI Blog Generator", layout="wide")

st.title("📝 AI Blog Generator")
st.markdown("Enter a topic, and let AI generate a blog post.")

question = st.text_input("Enter your blog topic/question")

if st.button("Generate Blog") and question:
    with st.spinner("Generating blog..."):
        keyword = extract_keyword(question)
        agent = CoordinatorAgent()
        result = agent.answer(question, keyword)

    st.success("✅ Blog Generated!")

    # ✅ Show only summary and blog post
    st.subheader("📄 Blog Summary")
    st.write(result["summary"])

    st.subheader("📝 Blog Post")
    st.markdown(result["blog_post"])

    st.download_button("📥 Download Markdown", data=result["blog_post"], file_name="blog.md")
