
def create_retriever(vector_store):
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "lambda_mult": 0.7}
    )

def create_retriever_pinecone(vector_store, k=3, score_threshold=0.4):
    return vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": k, "score_threshold": score_threshold},
)
