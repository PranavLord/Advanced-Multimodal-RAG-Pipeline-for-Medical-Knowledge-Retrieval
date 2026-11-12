# RAG Pipeline Structure & Flow

## What is RAG?
**RAG = Retrieval Augmented Generation**

User asks a question → System finds relevant documents → LLM generates answer using those documents → Return answer to user

---

## RAG Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER QUERY                              │
│                  "What is diabetes?"                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   1. INDEXING       │
        │ Split docs into     │
        │ small chunks        │
        │ + save to vector DB │
        └─────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   2. RETRIEVAL      │
        │ Search vector DB    │
        │ Find similar chunks │
        │ Get top 10 results  │
        └─────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   3. RANKING        │
        │ Reorder results     │
        │ Remove duplicates   │
        │ Get best 5 docs     │
        └─────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   4. GENERATION     │
        │ Send query + docs   │
        │ to LLM (Gemini)     │
        │ Generate answer     │
        └─────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   5. VALIDATION     │
        │ Check confidence    │
        │ Add citations       │
        │ Verify accuracy     │
        └─────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                   FINAL ANSWER                              │
│        "Diabetes is a condition where..."                   │
│        Confidence: 95%                                      │
│        Sources: [Doc1, Doc2, Doc3]                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
backend/rag/
├── indexing/           ← Step 1: Load & process documents
├── retrieval/          ← Step 2: Find relevant documents
├── ranking/            ← Step 3: Sort & filter results
├── generation/         ← Step 4: Generate LLM response
├── validation/         ← Step 5: Check quality & citations
├── pipeline.py         ← Main orchestrator (combines all steps)
└── utils.py            ← Helper functions
```

---

## Each Folder Will Contain:

### 1. **indexing/** - Load medical documents
- Read PDFs, images, text
- Split into meaningful chunks (by sections, not just size)
- Create embeddings
- Save to Pinecone vector database

### 2. **retrieval/** - Search for relevant chunks
- Take user query
- Convert to embedding
- Search Pinecone
- Return similar chunks + relevance score

### 3. **ranking/** - Sort results
- Take retrieved chunks
- Reorder by importance
- Remove duplicate info
- Keep top N best matches

### 4. **generation/** - Generate answer
- Combine query + top chunks
- Send to Gemini LLM
- LLM reads chunks and answers
- Return answer text

### 5. **validation/** - Quality checks
- Measure how confident the answer is
- Check if answer is supported by sources
- Add citations (which doc supports which claim)
- Add medical disclaimer if needed

### 6. **pipeline.py** - Orchestrator
- Connects all 5 steps
- Handles data flow
- Error handling
- Logging

### 7. **utils.py** - Helper functions
- Common utilities
- Text processing
- Embedding functions
- Database connections

---

## What You Need to Setup First

```
1. ✓ Folder structure (we're creating this now)
2. ✗ Python environment (venv or conda)
3. ✗ Install requirements.txt packages
4. ✗ Setup API keys (.env file)
   - GOOGLE_API_KEY (for Gemini)
   - PINECONE_API_KEY (for vector DB)
5. ✗ Create sample medical documents
6. ✗ Index documents (fill Pinecone)
```

---

## Then You're Ready to Learn Each Step

Once structure is done + env is setup:
- Step 1: Learn how to chunk medical docs
- Step 2: Learn how to search vectors
- Step 3: Learn how to rerank
- Step 4: Learn how to use Gemini LLM
- Step 5: Learn validation techniques

Each step will be IN ITS OWN FOLDER, so you know what to focus on!
