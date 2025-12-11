from flask import Flask, jsonify, render_template, request

import helpers

app = Flask(__name__)

CHUNK_PATH = "outputs/task_8_chunks.json"
EMBEDDING_PATH = "outputs/task_8_embeddings.pkl"
OUTPUT_PATH = "outputs/task_11.json"


def task_11():
    """
    Goal:
        Launch the Flask app which looks like Google with a nicer background where the user types a user query and outputs the insights and citations from the 3 files
    Instructions for task 11:
        - Create a Flask app with a query endpoint that returns insights and citations based on a user query.
        - Use the RAG mechanisms from tasks 8, 9, 10
        - You can copy paste the relevant code from those tasks into small helper functions here
        - Save the outputs in task_11.json
    """
    app.run(host="0.0.0.0", port=5600)


def load_vector_data():
    """Load the chunk metadata and embeddings so every request can reuse the cache."""
    import json
    import os
    import pickle

    if not os.path.exists(CHUNK_PATH) or not os.path.exists(EMBEDDING_PATH):
        raise FileNotFoundError("Run Task 8 to prepare chunks and embeddings first.")

    with open(CHUNK_PATH) as chunk_file:
        chunk_records = json.load(chunk_file)
    with open(EMBEDDING_PATH, "rb") as emb_file:
        embeddings = pickle.load(emb_file)
    if len(chunk_records) != len(embeddings):
        raise ValueError("Chunk metadata count does not match embeddings.")
    return chunk_records, embeddings


chunk_records, chunk_embeddings = load_vector_data()
model = None


def get_embedding_model():
    """Lazy-load the SentenceTransformer model to avoid costly startup per request."""
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def score_query_against_chunks(query, top_k=3):
    """Return the top-k chunk records together with their cosine score."""
    import math

    model = get_embedding_model()
    query_vector = model.encode(query, convert_to_numpy=True).tolist()

    def cosine_similarity(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    scored = []
    for meta, embedding in zip(chunk_records, chunk_embeddings):
        scored.append(
            {
                "chunk": meta,
                "score": cosine_similarity(embedding, query_vector),
            }
        )
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def format_context_entries(scored_chunks):
    """Prepare structured context entries that mention chunk metadata for the LLM prompt."""
    entries = []
    for idx, entry in enumerate(scored_chunks):
        chunk = entry["chunk"]
        formatted_text = f"{idx+1}. {chunk['chunk_id']} [{chunk.get('source_file', 'unknown')}]: {chunk['text']}"
        entries.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source_file": chunk.get("source_file", "unknown"),
                "text": chunk["text"],
                "score": entry["score"],
                "formatted": formatted_text,
            }
        )
    return entries


def generate_insights(query, context_entries):
    """Invoke the LLM with structured instructions referencing the retrieved chunks."""
    prompt = f"""
    You are an analyst answering a research question using retrieved evidence.
    Generate at least three insights. Each insight must include an explanation (justification) and a citation pointing to the source_file or chunk_id.

    Query:
    {query}

    Retrieved context:
    {"".join(f"- {item['formatted']}\\n" for item in context_entries)}

    Return a JSON object that looks like:
    {{
        "insights": [
            {{
                "insight": "<final answer>",
                "justification": "<why the chunk supports the answer>",
                "citation": "<source_file or chunk_id>"
            }}
        ]
    }}
    """

    llm = helpers.LlmModel()
    response = llm.prompt_llm(prompt, get_structured_output="json")
    return response


@app.route("/", methods=["GET"])
def home():
    """Render the search UI from the templates directory."""
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query_insights():
    """Endpoint used by the UI that returns structured insights plus citations."""
    data = request.get_json(force=True)
    query_text = (data or {}).get("query", "").strip()
    if not query_text:
        return jsonify(error="Please provide a query."), 400

    scored = score_query_against_chunks(query_text, top_k=3)
    context_entries = format_context_entries(scored)
    structured = generate_insights(query_text, context_entries)
    structured_payload = {
        **structured,
        "retrieved_chunks": context_entries,
    }

    helpers.save_json(
        {
            "query": query_text,
            "retrieved_chunks": structured_payload["retrieved_chunks"],
            "insights": structured_payload.get("insights", []),
        },
        OUTPUT_PATH,
    )

    return jsonify(structured_payload)


if __name__ == "__main__":
    task_11()
