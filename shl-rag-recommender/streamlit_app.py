# streamlit_app.py
import streamlit as st
import requests

st.set_page_config(page_title="SHL RAG Recommender", layout="wide")

API_URL = "https://your-render-api-url.onrender.com/ask"  # Replace after Render deployment

st.title("🔍 SHL Assessment Recommender")

query = st.text_input("Describe the job requirement or candidate profile:")

k = st.slider("Number of relevant assessments to retrieve", 1, 10, 5)

if st.button("Find Recommendations") and query:
    with st.spinner("Fetching recommendations..."):
        params = {"query": query, "k": k}
        try:
            response = requests.get(API_URL, params=params)
            data = response.json()
            st.subheader("🔎 Recommendations:")
            for item in data["results"]:
                st.markdown(f"### [{item['test_name']}]({item['test_url']})")
                st.markdown(f"- **Duration**: {item.get('assessment_length', 'N/A')}")
                st.markdown(f"- **Job Levels**: {item.get('job_levels', 'N/A')}")
                st.markdown(f"- **Languages**: {item.get('languages', 'N/A')}")
                st.markdown(f"- **Description**: {item.get('description', 'N/A')}")
                st.markdown("---")
        except Exception as e:
            st.error(f"Error: {e}")
