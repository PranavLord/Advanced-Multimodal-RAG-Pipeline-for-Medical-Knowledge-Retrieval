# SETUP GUIDE - Before You Start Learning RAG

## Step 1: Create Python Environment

```bash
# Using venv (recommended)
cd d:\Pranav\Project\Machine-Learning\Advanced-Multimodal-RAG-Pipeline-for-Medical-Knowledge-Retrieval

# Create environment
python -m venv venv

# Activate it
venv\Scripts\activate

# On Linux/Mac:
# source venv/bin/activate
```

---

## Step 2: Install Requirements

```bash
# Make sure venv is activated, then:
pip install -r backend/requirements.txt
```

This will install:
- LangChain (RAG orchestration)
- Pinecone (vector database)
- Google Gemini (LLM)
- Sentence Transformers (embeddings)
- PyMuPDF (read PDFs)
- And more...

---

## Step 3: Setup API Keys

Create `.env` file in project root:

```
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=medical-rag-index
```

**Where to get keys:**
1. **Google API Key**: https://console.cloud.google.com/apis/credentials
   - Enable Generative AI API
   - Create service account key
   
2. **Pinecone API Key**: https://www.pinecone.io/
   - Create account
   - Create project
   - Copy API key

---

## Step 4: Verify Setup

Run this to check everything works:

```bash
python -c "import langchain; import pinecone; import google.generativeai; print('✓ All packages installed!')"
```

---

## THEN YOU'RE READY!

Once environment is setup + API keys are configured, you can:

1. Learn how to **INDEX** medical documents
2. Learn how to **RETRIEVE** similar documents  
3. Learn how to **RANK** results
4. Learn how to **GENERATE** answers
5. Learn how to **VALIDATE** answers

Each folder has clear purpose + examples!

---

## Checklist Before Learning:

- [ ] Created venv
- [ ] Activated venv
- [ ] Installed requirements.txt
- [ ] Created .env with API keys
- [ ] Verified imports work
- [ ] Understand RAG flow (see README.md)
- [ ] Ready to learn Step 1: Indexing!
