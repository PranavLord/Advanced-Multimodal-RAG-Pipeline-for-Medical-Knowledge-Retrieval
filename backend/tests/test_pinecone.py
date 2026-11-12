from core.vectorstore_manager.pinecone_manager import (
    PineconeManager
)


pinecone = PineconeManager()

print(
    pinecone.describe()
)