### rag_api.py

import os
import faiss
import pickle
import numpy as np
from flask import Flask, request, jsonify
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore import InMemoryDocstore
import google.generativeai as genai

app = Flask(__name__)

# Load FAISS index
index = faiss.read_index("data/shl_index.faiss")
with open("data/shl_metadata.pkl", "rb") as f:
    docstore = pickle.load(f)

index_to_docstore_id = {i: str(i) for i in range(index.ntotal)}
vectorstore = FAISS(
    embedding_function=None,
    index=index,
    docstore=InMemoryDocstore(docstore),
    index_to_docstore_id=index_to_docstore_id,
)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def format_docs_for_gemini(docs):
    formatted = []
    for doc in docs:
        metadata = doc.metadata
        formatted.append(
            f"name: {metadata.get('name', '')}\n"
            f"remote_testing: {metadata.get('remote_testing', '')}\n"
            f"adaptive_irt: {metadata.get('adaptive_irt', '')}\n"
            f"assessment_types: {metadata.get('assessment_types', '')}\n"
            f"description: {metadata.get('description', '')}\n"
            f"job_levels: {metadata.get('job_levels', '')}\n"
            f"languages: {metadata.get('languages', '')}\n"
            f"assessment_length: {metadata.get('assessment_length', '')}\n"
        )
    return "\n---\n".join(formatted)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    query = data.get("query", "")
    top_k = int(data.get("top_k", 3))

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    # Embed the query
    query_embedding = embedding_model.embed_query(query)

    # Retrieve top 20 documents
    docs = vectorstore.similarity_search_by_vector(query_embedding, k=20)
    formatted_docs = format_docs_for_gemini(docs)

    prompt = (
        "You are an assistant that helps recommend assessments from a list."
        " Given the following assessments and the user query, return the names of the top"
        f" {top_k} most relevant assessments in order of relevance.\n\n"
        f"Assessments:\n{formatted_docs}\n\nQuery: {query}\n\n"
        "Return a list of the top assessments' names only in order."
    )

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt,
    generation_config={
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 1024
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 3},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 3},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 3},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": 3},
    ]
)
    recommended_names = response.text.strip().split("\n")

    results = []
    for name in recommended_names:
        for doc in docs:
            if doc.metadata.get("name", "").strip().lower() == name.strip().lower():
                results.append({
                    "name": doc.metadata.get("name", ""),
                    "url": doc.metadata.get("url", ""),
                    "remote_testing": doc.metadata.get("remote_testing", ""),
                    "adaptive_irt": doc.metadata.get("adaptive_irt", ""),
                    "assessment_length": doc.metadata.get("assessment_length", ""),
                    "assessment_types": doc.metadata.get("assessment_types", ""),
                })
                break

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)

