import helpers


def task_8():
    """
    Goal:
        Chunk the three needle-in-haystack files, embed every chunk, and save the data for retrieval.
    Instructions:
        - Load the three needle-in-haystack files from the outputs/task_7_file_1.txt, outputs/task_7_file_2.txt, and outputs/task_7_file_3.txt
        - Chunk the three files into chunks of 64 tokens with 12 token overlap
        - Embed each chunk using Sentence Transformers
        - Save the chunks and embeddings to the outputs/task_8_chunks.json and outputs/task_8_embeddings.pkl
    """

    import json
    import os
    import pickle
    from pathlib import Path

    from sentence_transformers import SentenceTransformer

    chunk_size = 64
    overlap = 12
    sources = [
        Path("outputs/task_7_file_1.txt"),
        Path("outputs/task_7_file_2.txt"),
        Path("outputs/task_7_file_3.txt"),
    ]
    chunk_records = []
    chunk_texts = []

    # Split each source into fixed-size word buckets and record metadata.
    for path in sources:
        if not path.exists():
            raise FileNotFoundError(f"{path} not found. Run task 7 first.")

        text = helpers.load_txt(str(path)).strip()
        if not text:
            continue

        words = text.split()
        step = chunk_size - overlap
        for idx in range(0, len(words), step):
            chunk_words = words[idx : idx + chunk_size]
            chunk_text = " ".join(chunk_words).strip()
            if not chunk_text:
                continue

            chunk_record = {
                "chunk_id": f"{path.name}_{idx // chunk_size}",
                "source_file": path.name,
                "chunk_index": idx // chunk_size,
                "text": chunk_text,
            }
            chunk_records.append(chunk_record)
            chunk_texts.append(chunk_text)

    if not chunk_records:
        raise ValueError("No content found in Task 7 outputs.")

    # Embed each chunk using Sentence Transformers.
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = [vector.tolist() for vector in model.encode(chunk_texts)]

    # Persist chunks metadata and embeddings to disk.
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    helpers.save_json(chunk_records, "outputs/task_8_chunks.json")
    helpers.save_pickle(embeddings, "outputs/task_8_embeddings.pkl")