# Understanding RAG Architecture - Two Folders Explained

## Two Different Folders, Two Different Purposes

### 1. `backend/core/rag_retrieval/` - UTILITY LAYER
**What goes here:**
- Basic retrieval functions
- Low-level vector database operations
- Raw embeddings operations
- Database connection utilities

**Purpose:** 
- Reusable utilities
- Shared by multiple systems
- NOT the main RAG pipeline

**Example:**
```python
# backend/core/rag_retrieval/
def get_vector_from_db(query, top_k):
    """Low-level: Get raw vectors from Pinecone"""
    pass

def create_embedding(text):
    """Low-level: Convert text to embedding"""
    pass
```

---

### 2. `backend/rag/` - MAIN RAG PIPELINE (5 STEPS)
**What goes here:**
- Complete RAG workflow
- Orchestration of 5 steps
- Business logic
- Medical-specific features

**The 5 Steps:**

```
Step 1: INDEXING (indexing/)
├── Load medical documents
├── Split into chunks
├── Create embeddings
└── Save to Pinecone

Step 2: RETRIEVAL (retrieval/)
├── Take user query
├── Convert to embedding
├── Search Pinecone
└── Return top 10 chunks

Step 3: RANKING (ranking/)
├── Reorder chunks
├── Remove duplicates
├── Calculate relevance scores
└── Keep best 5

Step 4: GENERATION (generation/)
├── Combine query + chunks
├── Send to Gemini LLM
├── LLM reads & thinks
└── Generate answer

Step 5: VALIDATION (validation/)
├── Check confidence
├── Add citations
├── Verify medical accuracy
└── Add disclaimers
```

---

## How They Work Together

```
┌──────────────────────────────────────────────┐
│  backend/rag/ (Main RAG Pipeline)            │
│                                              │
│  Step 1: INDEXING                            │
│    └─→ Uses: core/rag_retrieval/             │
│        (create_embedding, save_to_db)        │
│                                              │
│  Step 2: RETRIEVAL                           │
│    └─→ Uses: core/rag_retrieval/             │
│        (get_vector_from_db)                  │
│                                              │
│  Step 3-5: RANKING, GENERATION, VALIDATION   │
│    └─→ Uses: core/ modules + Gemini API      │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Analogy

Think of it like a **Restaurant:**

- **`backend/core/rag_retrieval/`** = Kitchen utilities
  - Knife (cut vegetables)
  - Stove (heat food)
  - Fridge (store ingredients)
  - Reusable tools

- **`backend/rag/`** = Complete Recipe
  - Step 1: Prep ingredients (use knife)
  - Step 2: Cook (use stove)
  - Step 3: Plate nicely
  - Step 4: Serve to customer
  - Step 5: Customer feedback

---

## What Code Goes Where

### `backend/core/rag_retrieval/`
```python
# Low-level operations
def embed_text(text):
    return model.encode(text)

def search_vector_db(embedding, top_k):
    return pinecone_index.query(embedding, top_k=top_k)

def save_to_vector_db(text, embedding, metadata):
    pinecone_index.upsert([(id, embedding, metadata)])
```

### `backend/rag/indexing/`
```python
# High-level: Uses core/rag_retrieval
from backend.core.rag_retrieval import embed_text, save_to_vector_db

def index_medical_document(doc_path):
    # 1. Load document
    text = load_pdf(doc_path)
    
    # 2. Split into chunks
    chunks = chunk_text(text)
    
    # 3. Embed (uses core utility)
    embeddings = [embed_text(chunk) for chunk in chunks]
    
    # 4. Save (uses core utility)
    for chunk, embedding in zip(chunks, embeddings):
        save_to_vector_db(chunk, embedding, metadata)
```

### `backend/rag/retrieval/`
```python
# High-level: Uses core/rag_retrieval
from backend.core.rag_retrieval import embed_text, search_vector_db

def retrieve_documents(query):
    # 1. Embed query (uses core utility)
    query_embedding = embed_text(query)
    
    # 2. Search (uses core utility)
    results = search_vector_db(query_embedding, top_k=10)
    
    # 3. Process results
    return format_results(results)
```

---

## Summary

| Aspect | `core/rag_retrieval/` | `rag/` |
|--------|----------------------|---------|
| **Purpose** | Low-level utilities | Main pipeline |
| **What's here** | Basic functions | 5-step workflow |
| **Reusable** | Yes (by other systems) | No (RAG-specific) |
| **Dependencies** | Minimal (just DB/LLM) | Uses core/ + others |
| **Learn first** | Yes (understand basics) | Then (build on basics) |

---

## Your Learning Path

1. **First:** Understand `backend/core/rag_retrieval/` - The toolkit
2. **Then:** Build `backend/rag/` - Use the toolkit to build RAG

Think of it as:
- Core = LEGO blocks
- RAG = Building with LEGO blocks

You need to understand the blocks first, then build the castle!
