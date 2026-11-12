# Quick Reference - What Goes Where

## Simple Answer

```
backend/core/rag_retrieval/        backend/rag/
     (UTILITIES)                  (MAIN PIPELINE)
        ↓                              ↓
   Reusable tools          Complete RAG system
   (Low-level)             (5 clear steps)
   
   - embed_text()          Step 1: indexing/
   - search_db()           Step 2: retrieval/
   - save_db()             Step 3: ranking/
   - format()              Step 4: generation/
                           Step 5: validation/
                           
   Used BY:                Orchestrates:
   ├─ backend/rag/         ├─ backend/core/
   ├─ api/                 ├─ Pinecone
   └─ other systems        ├─ Gemini LLM
                           └─ Medical logic
```

---

## Code Examples - What Goes In Each

### `backend/core/rag_retrieval/operations.py`
```python
# UTILITY LAYER - Low-level operations

def embed_query(query: str) -> list:
    """Convert text to embedding vector"""
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embedding_model.encode(query).tolist()


def search_pinecone(embedding: list, top_k: int = 10):
    """Raw Pinecone search - returns vectors only"""
    index = get_pinecone_index()
    results = index.query(embedding, top_k=top_k, include_metadata=True)
    return results


def save_to_pinecone(vectors: list, metadata: dict):
    """Save vectors to Pinecone - no processing"""
    index = get_pinecone_index()
    index.upsert(vectors)
```

---

### `backend/rag/retrieval/__init__.py`
```python
# MAIN PIPELINE LAYER - Orchestrated retrieval

from backend.core.rag_retrieval import embed_query, search_pinecone

class MedicalDocumentRetriever:
    """Step 2 of RAG Pipeline: RETRIEVE"""
    
    def retrieve(self, user_query: str) -> list:
        """
        1. Use core utility to embed query
        2. Use core utility to search
        3. Add medical-specific logic
        4. Return formatted results
        """
        
        # Step 1: Use core utility
        query_embedding = embed_query(user_query)
        
        # Step 2: Use core utility
        raw_results = search_pinecone(query_embedding, top_k=10)
        
        # Step 3: Add medical logic
        filtered = self._filter_medical_results(raw_results)
        scored = self._score_relevance(filtered)
        
        # Step 4: Return formatted
        return self._format_for_next_step(scored)
    
    def _filter_medical_results(self, results):
        """Medical-specific filtering"""
        pass
    
    def _score_relevance(self, results):
        """Calculate relevance scores"""
        pass
    
    def _format_for_next_step(self, results):
        """Prepare for ranking step"""
        pass
```

---

## The Flow

```
User Query
    ↓
┌─────────────────────────────────────┐
│  backend/rag/retrieval/             │  MAIN LOGIC
│  class MedicalDocumentRetriever     │
│        ↓                            │
│        └─→ calls: embed_query()     │  Uses UTILITIES
│               (from core/)          │
│        ↓                            │
│        └─→ calls: search_pinecone() │  Uses UTILITIES
│               (from core/)          │
│        ↓                            │
│        └─→ Add medical logic        │  MAIN LOGIC
│        ↓                            │
│  Returns formatted results          │
└─────────────────────────────────────┘
    ↓
Pass to Step 3: ranking/
```

---

## Decision: Use Both or Just One?

**RECOMMENDED:**

✅ **Use BOTH**
- `backend/core/rag_retrieval/` = Utilities (reusable)
- `backend/rag/` = Main pipeline (orchestrator)
- Clean separation
- Can reuse utilities elsewhere

❌ **Don't put everything in one folder**
- Would be messy
- Hard to reuse
- Violates architecture

---

## Files to Create

### In `backend/core/rag_retrieval/`:
- `__init__.py` - Export utilities
- `operations.py` - Basic DB operations
- `embeddings.py` - Embedding operations
- `vector_store.py` - Vector store operations

### In `backend/rag/`:
- `indexing/` - Uses core utilities to INDEX
- `retrieval/` - Uses core utilities to RETRIEVE
- `ranking/` - Reranks results
- `generation/` - Uses Gemini to generate
- `validation/` - Validates and cites
- `pipeline.py` - Orchestrator (connects all)

---

## TL;DR

**`core/rag_retrieval/`** = Tools in toolbox
**`backend/rag/`** = Building with tools

Both needed. Both important. Different purposes.
