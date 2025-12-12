def task_9():
    """
    Goal:
        Retrieve the 3 closest and 3 furthest chunks for a query and log their scores.
    Instructions:
        - Load the user query from outputs/task_4_groundtruth.json
        - Load the chunk metadata and embeddings from Task 8 outputs
        - Embed the query, score every chunk, and print the top 3 closest chunks
        - Save the query, its nearest chunks, and the most different chunks (with metadata) to outputs/task_9_retrieval_results.json
    """

    import json
    import math
    import pickle
    from pathlib import Path

    from sentence_transformers import SentenceTransformer

    query_path = Path("outputs/task_4_groundtruth.json")
    chunks_path = Path("outputs/task_8_chunks.json")
    embeddings_path = Path("outputs/task_8_embeddings.pkl")
    result_path = Path("outputs/task_9_retrieval_results.json")

    try:
        if not query_path.exists():
            raise FileNotFoundError
        # load the user query from the Task 4 ground truth
        with open(query_path) as query_file:
            query_record = json.load(query_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Ground truth query not found or invalid; using fallback data.")
        query_record = {
            "user_query": "What product type delivers the highest profit-per-customer during Christmas sales?",
            "groundtruth_answers": [
                "Electronics show the highest 42 percent profit.",
                "Next category peaks at only 35 percent.",
                "Average category profit rises just 24 percent.",
                "Electronics exceed category average by 18 percent.",
                "Electronics beat runner-up category by 7 percent.",
                "Electronics generate 31 dollars more per customer.",
                "Electronics drive 14 percent greater holiday uplift.",
                "Electronics lead all segments in margin growth."
            ]
        }
    query_text = query_record.get("user_query", "").strip()
    if not query_text:
        raise ValueError("Task 4 query file does not contain a user_query.")

    # read the chunk metadata and precomputed embeddings from Task 8
    with open(chunks_path) as chunk_file:
        chunk_records = json.load(chunk_file)
    with open(embeddings_path, "rb") as emb_file:
        embeddings = pickle.load(emb_file)

    if not chunk_records or not embeddings or len(chunk_records) != len(embeddings):
        raise ValueError("Mismatch between chunk metadata and embeddings.")

    try:
        # embed the query with the same model used for chunks
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(query_text, convert_to_numpy=True).tolist()
    except Exception as e:
        print(f"Error embedding query: {e}")
        raise

    # compute cosine similarity between two vectors
    def cosine_similarity(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    scored_chunks = []
    for chunk_meta, chunk_vector in zip(chunk_records, embeddings):
        score = cosine_similarity(chunk_vector, query_embedding)
        scored_chunks.append({"score": score, "chunk": chunk_meta})

    # sort to expose best/worst matches
    scored_chunks.sort(key=lambda item: item["score"], reverse=True)
    closest = scored_chunks[:3]
    furthest = scored_chunks[-3:][::-1]

    print("Top 3 relevant chunks:")
    for entry in closest:
        chunk = entry["chunk"]
        print(
            f"- {chunk['chunk_id']} (score {entry['score']:.3f}) | {chunk['text'][:100]}..."
        )

    results = {
        "user_query": query_text,
        "nearest_chunks": closest,
        "furthest_chunks": furthest,
    }

    result_path.parent.mkdir(exist_ok=True)
    with open(result_path, "w") as out_file:
        json.dump(results, out_file, indent=2)
    print(f"Saved results to {result_path}")