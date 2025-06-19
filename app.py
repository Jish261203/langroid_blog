import streamlit as st
from agents.coordinator_agent import CoordinatorAgent
from run_example import extract_keyword
import json

st.set_page_config(page_title="AI Blog Generator", layout="wide")

st.title("📝 AI Blog Generator")
st.markdown("Enter a topic, and let AI generate a blog post.")

question = st.text_input("Enter your blog topic/question")

if st.button("Let see the Magic🪄") and question:
    with st.spinner("Thinking 🤔..."):
        keyword = extract_keyword(question)
        agent = CoordinatorAgent()
        result = agent.answer(question, keyword)

    st.success("✅ Blog Generated!")

    # ✅ Show only summary and blog post
    st.subheader("📄 Blog Summary")
    st.write(result["summary"])

    st.subheader("📝 Blog Post")
    st.markdown(result["blog_post"])

    # Show search results (title and snippet) in the UI if available
    search_results = result.get("search_results_json", "[]")
    try:
        search_results_list = json.loads(search_results)
    except Exception:
        search_results_list = []
    if search_results_list:
        st.subheader("🔎 Search Results")
        for i, hit in enumerate(search_results_list, 1):
            st.markdown(f"**{i}. {hit.get('title', '')}**\n\n{hit.get('snippet', '')}")

    # Prepare full output to download in the required format
    full_output = f"""{question}

[Using target keyword: {keyword}]

```json
{result.get('search_results_json', '[]')}
```
{result["summary"]}
```json
{json.dumps(result["seo"], indent=2, ensure_ascii=False)}
```
{result["blog_post"]}

{json.dumps(result, indent=2, ensure_ascii=False)}
"""

    st.download_button(
        label="📥 Download Blog",
        data=full_output,
        file_name="blog_output.md",
        mime="text/markdown"
    )