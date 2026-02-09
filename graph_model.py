from typing import List
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.documents import Document
#Chroma Vector Store
from build_vectore import get_vector_store
from retriever import create_retriever
#Pinecone Vector Store
from build_vectore_pinecone import create_pinecone_vector_store
from retriever import create_retriever_pinecone


from llm import create_chat


class State(MessagesState):
    documents: List[Document]


def retrieve_documents(state: State) -> State:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    #Chroma Vector Store
    # vector_store = get_vector_store(embeddings)
    # retriever = create_retriever(vector_store)

    #Pinecone Vector Store
    vector_store = create_pinecone_vector_store("langchain-test-index", embeddings)
    retriever = create_retriever_pinecone(vector_store, k=10, score_threshold=0.4)

    query = state["messages"][-1].content
    docs = retriever.invoke(query)

    # document_pages = [doc.page_content for doc in docs]

    return {"documents": docs}

def re_rank_documents(state: State) -> State:
    chat = create_chat("gemini")
    documents = state["documents"]
    query = state["messages"][-1].content

    prompt = f"""
    You are a ranking assistant.

    Given the query:
    "{query}"

    Rank the following documents by relevance.
    Return ONLY a Python list of integer indices (e.g. [2, 0, 1]).
    Do not add explanation.

    Documents:
    {[(i, d.page_content[:500]) for i, d in enumerate(documents)]}
    """
    response = chat.invoke(prompt)
    try:
        ranked_indices = eval(response.content)
        ranked_indices = [
            i for i in ranked_indices
            if isinstance(i, int) and 0 <= i < len(documents)
        ]
    except Exception:
        ranked_indices = list(range(len(documents)))  # fallback

    top_documents = [documents[i] for i in ranked_indices[:5]]

    # document_pages = [doc.page_content for doc in top_documents]

    return {"documents": top_documents}


def generate_answer(state: State) -> State:
    chat = create_chat("gemini")
    documents = state["documents"]
    question = state["messages"][-1].content

    # Build citation-aware context
    formatted_docs = []
    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown Source")
        title = doc.metadata.get("title", "Untitled")
        page = doc.metadata.get("page", "N/A")
        # print( f"Document {i} source: {source}, title: {title}" )
        formatted_docs.append(
            f"[{i}] Source: {source}\n{doc.page_content}"
        )

    context = "\n\n".join(formatted_docs)

    prompt = f"""
Use ONLY the documents below to answer the question.

Documents:
{context}

Question:
{question}

Rules:  
- Cite sources using footnotes like [1], [2]
- Each factual sentence MUST have a footnote
- In last, provide a list of sources used based on footnotes
- Keep the answer concise and to the point
- If the answer is not present, say:DDD
  "I don't find the answer in the provided documents."
"""

    response = chat.invoke(prompt)

    return {
        "messages": state["messages"] + [response]
    }



def build_graph():
    graph = StateGraph(State)

    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("re_rank_documents", re_rank_documents)

    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents", "re_rank_documents")
    graph.add_edge("re_rank_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

if __name__ == "__main__":
    graph = build_graph()
    mermaid = graph.get_graph().draw_mermaid()
    print(mermaid)


