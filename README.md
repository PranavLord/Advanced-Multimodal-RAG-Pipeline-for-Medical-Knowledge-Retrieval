# 🏥 Advanced Multimodal RAG Pipeline for Medical Knowledge Retrieval

A production-grade Retrieval-Augmented Generation (RAG) system for analyzing medical documents and images using advanced AI techniques.

## 📊 Project Structure

```
Advanced-Multimodal-RAG-Pipeline-for-Medical-Knowledge-Retrieval/
│
├── backend/                           # FastAPI Backend
│   ├── core/
│   │   ├── llm/                       # Gemini LLM interactions & reasoning
│   │   ├── rag_retrieval/             # Hybrid search, reranking, retrieval
│   │   ├── query_processors/          # Query expansion, HyDE, decomposition
│   │   ├── embeddings/                # PubMedBERT embedding generation
│   │   ├── vectorstore_manager/       # Pinecone operations & indexing
│   │   └── validators/                # Self-RAG, CRAG, confidence scoring
│   ├── document_processors/           # PDF parsing, OCR, image processing
│   ├── api/
│   │   ├── routes/                    # FastAPI endpoints
│   │   └── models/                    # Request/response schemas
│   ├── config/                        # Settings & prompts
│   ├── utils/                         # Helper functions & logging
│   ├── data/
│   │   ├── sample_reports/            # Medical reports
│   │   ├── sample_images/             # X-rays, MRIs
│   │   ├── medical_guidelines/        # Reference documents
│   │   └── drug_database/             # Drug interactions
│   └── requirements.txt
│
├── frontend/                          # Streamlit Frontend
│   ├── components/                    # UI components
│   ├── pages/                         # Streamlit pages
│   ├── utils/                         # API helpers
│   └── requirements.txt
│
├── .env.template                      # Environment variables template
├── .gitignore
└── README.md

```

## 🎯 16 Advanced RAG Techniques

### Indexing (3)
- ✅ Semantic Chunking
- ✅ Hierarchical Indexing
- ✅ Parent-Child Document Retrieval

### Query Transformation (3)
- ✅ Query Expansion
- ✅ HyDE (Hypothetical Document Embeddings)
- ✅ Query Decomposition

### Retrieval (3)
- ✅ Hybrid Search (Vector + BM25)
- ✅ Multi-Vector Retrieval
- ✅ Metadata Filtering

### Reranking (1)
- ✅ Cross-Encoder Reranking

### Generation (2)
- ✅ Chain-of-Thought Prompting
- ✅ Context Compression

### Validation (4)
- ✅ Self-RAG
- ✅ CRAG (Corrective RAG)
- ✅ Confidence Scoring
- ✅ Citation Grounding

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Gemini 2.0 Flash (Multimodal) |
| Vector DB | Pinecone |
| Embeddings | PubMedBERT (768-dim) |
| Framework | LangChain |
| Frontend | Streamlit |
| Backend API | FastAPI |
| Doc Processing | PyMuPDF, Tesseract OCR |
| Evaluation | RAGAS |

## 📋 Getting Started

### Step 1: Setup Environment
```bash
# Copy template to .env and fill in your API keys
cp .env.template .env
```

### Step 2: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```bash
cd frontend
pip install -r requirements.txt
```

### Step 4: Start Backend
```bash
cd backend
python main.py
```

### Step 5: Start Frontend
```bash
cd frontend
streamlit run app.py
```

## 📝 API Keys Required

- **Pinecone** - Vector database
- **Google AI Studio** - Gemini LLM
- **HuggingFace** - PubMedBERT embeddings
- **Cohere** (Optional) - Reranking

## 🚀 Performance Targets

- **Trust Level**: 85-90% accuracy
- **Response Time**: <5 seconds
- **Hallucination Rate**: <5%
- **Citation Coverage**: 100%

## 📚 Learn Step-by-Step

This project is designed for learning. Each component is modular and can be understood independently:

1. **Backend Setup** - Understand data flow
2. **Document Processing** - Learn chunking & embeddings
3. **RAG Retrieval** - Explore search techniques
4. **LLM Integration** - See reasoning in action
5. **Validation** - Implement safety guardrails
6. **Frontend** - Build the UI

---

**Status**: Initial folder structure created ✅
**Next Step**: Wait for your instructions to proceed!

