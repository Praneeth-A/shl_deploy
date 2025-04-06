# streamlit_app.py

### streamlit_app.py

import requests
import streamlit as st

st.title("SHL Assessment Recommender")

query = st.text_input("Enter your goal, job, or skill (e.g., software developer role)")
top_k = st.slider("Number of assessments to recommend", min_value=1, max_value=10, value=3)

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        response = requests.post(
            " https://shl-deploy.onrender.com/recommend",
            json={"query": query, "top_k": top_k},
        )
        if response.status_code == 200:
            results = response.json()["results"]
            for r in results:
                st.markdown(f"**[{r['name']}]({r['url']})**")
                st.markdown(f"- Remote Testing: {r['remote_testing']}")
                st.markdown(f"- Adaptive/IRT Support: {r['adaptive_irt']}")
                st.markdown(f"- Duration: {r['assessment_length']}")
                st.markdown(f"- Type: {r['assessment_types']}")
                st.markdown("---")



