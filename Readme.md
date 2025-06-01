# 🧠 SHL GenAI Assessment Recommendation Tool

This project recommends the most relevant SHL assessments based on user queries using a RAG (Retrieval-Augmented Generation) pipeline with FAISS and Gemini Pro. It features a Streamlit frontend and a Flask backend, powered by vector similarity search and LLM ranking.

---

## 📁 Repository Structure

```bash
shlbackend/ @ commit 55546bf
├── data/                        # FAISS index and .pkl metadata
│   ├── shl_index.faiss
│   └── docstore.pkl
├── onnx_model/                 # Optional: used if embedding model is optimized
├── rag_api.py                  # Main Flask backend for RAG
├── requirements.txt            # Backend dependencies

shlfrontend/ @ commit 80d7f2b
├── streamlit_app.py            # Streamlit frontend
├── requirements.txt            # Frontend dependencies

shlScrapedData.json             # Contains scraped data from shl website
embeddingDocs.py                # Script to embed scraped data into FAISS index + pkl
webScraping.py                  # Script to scrape SHL catalog and tests
problemApproach.pdf             # Detailed explaination of approach to problem statement
```

---

## ⚙️ Prerequisites

- Python 3.9 or later
- pip
- Git

---

## 🔄 Setup Instructions (Windows)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/shl-assessment-recommender.git
cd shl-assessment-recommender
```

### 2. 🔙 Setup Backend
```bash
cd shlbackend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the backend (Flask)
python rag_api.py
```
Flask will run on `http://localhost:8000`.


### 3. 🖥️ Setup Frontend
Open a new terminal:
```bash
cd shlfrontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the frontend (Streamlit)
streamlit run streamlit_app.py
```
Frontend will open in your browser at `http://localhost:8501`


### 4. Optional: 🔁 Rebuild FAISS index
If needed, you can re-scrape and re-embed the data:
```bash
python webScraping.py        # Scrape SHL test data
python embeddingDocs.py      # Convert to embeddings, save FAISS and pkl
```
This will regenerate the FAISS index and `docstore.pkl` files.

---

## 🌐 API Endpoint

- `POST /recommend` at `http://localhost:8000`
- 📤 Request JSON:
```json
{
  "query": "I need a test for logical reasoning"
}
```
- 📥 Response JSON:
```json
[
  {
    "assessment_name": "Numerical Reasoning Test",
    "url": "https://...",
    "remote_testing": "Yes",
    "adaptive_irt": "No",
    "assessment_length": "30 minutes",
    "assessment_types": "Cognitive"
  },
  ...
]
```

---

## 🤖 Technologies Used
- Python 3.9+
- Flask (API backend)
- Streamlit (frontend UI)
- FAISS (vector similarity search)
- LangChain (retrieval wrapper)
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- Google Gemini Pro (LLM ranking)
- ONNX (optional model optimization)

---

## 📌 Setup Tips & Configuration

### 🔐 Setting Your Gemini API Key
To access Gemini, set your API key as an environment variable **before running the backend**:

```bash
# Windows CMD
set GOOGLE_API_KEY=your-api-key

# PowerShell
$env:GOOGLE_API_KEY="your-api-key"
```

---

### ✅ Optional: Using `.env` File (more convenient)
Prefer using a `.env` file instead of typing your key every time?

1. **Modify `rag_api.py` to include:**
```python
from dotenv import load_dotenv
load_dotenv()
```

2. **Create a `.env` file in `shlbackend/` with:**
```env
GOOGLE_API_KEY=your-api-key
```

> 💡 Remember to add `.env` to `.gitignore` so you don’t commit your secrets.

---

--The FAISS index and `.pkl` files must match the order and content of embedded documents.

--If using ONNX model for embedding speed, adjust `embeddingDocs.py` to load from `onnx_model/`.

---

## 📬 Questions or Issues?
Open an issue on GitHub or contact me.

