import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from uuid import uuid4
from generate_pdf import load_pdf
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

# dim = len(embeddings.embed_query("test"))
# print("Actual embedding dimension:", dim)

assert len(embeddings.embed_query("test")) == 3072

index_name = "langchain-test-index"


def initialize_pinecone_vector_store(index_name, embeddings):
    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    indexes = pc.list_indexes().names()
    if index_name in indexes:
        print(f"Index '{index_name}' already exists. Deleting it for recreation.")
        pc.delete_index(index_name)
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    index = pc.Index(index_name)
    return PineconeVectorStore(index=index, embedding=embeddings)


def embed_documents_to_pinecone(vector_store, documents, category="default"):
    uuids = [str(uuid4()) for _ in documents]
    vector_store.add_documents(documents=documents, ids=uuids, category=category)
    print(f"Embedded {len(documents)} documents into Pinecone index '{index_name}' with category '{category}'.")


documents = load_pdf("documents/big_data_analytics.pdf")
print(f"Loaded {len(documents)} documents from PDF.")
vector_store = initialize_pinecone_vector_store(index_name, embeddings)
print("Initialized Pinecone vector store.")
embed_documents_to_pinecone(vector_store, documents)
print("Embedding process completed.")

# print(documents)

# def upload_embeddings_to_pinecone(embeddings, index, document, category="default"):
#     # Example data to upload
#     example_data = [
#         ("id1", embeddings.embed_query("Sample text 1")),
#         ("id2", embeddings.embed_query("Sample text 2")),
#         ("id3", embeddings.embed_query("Sample text 3")),
#     ]

#     # Prepare data for upsert
#     vectors = [(id, vector) for id, vector in example_data]

#     # Upsert data into Pinecone index
#     index.upsert(vectors=vectors)
#     print(f"Uploaded {len(vectors)} embeddings to Pinecone index '{index_name}'.")
