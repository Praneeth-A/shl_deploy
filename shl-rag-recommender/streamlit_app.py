# import streamlit as st

if __name__ == "__main__":
    import streamlit as st
    import requests

    st.title("SHL Assessment Recommender")

    query = st.text_input("Enter job description or requirement")

    if st.button("Get Recommendations"):
        if query:
            with st.spinner("Fetching recommendations..."):
                response = requests.post(
                    "https://shl-deploy.onrender.com/recommend",
                    json={"query": query}
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        st.markdown("### Recommended Assessments")
                        st.table(data)
                    else:
                        st.warning("No relevant assessments found.")
                else:
                    st.error("Error in retrieving recommendations.")
        # streamlit logic here
