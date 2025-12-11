import helpers


def task_10():
    """
    Goal:
        Combine retrieved chunks with the user query and generate an improved answer using the LLM with citations and evaluate the recall of the answer.
    Instructions:
        - Load the user query from the file outputs/task_4_groundtruth.json
        - Load the chunks and embeddings from the outputs/task_8_chunks.json and outputs/task_8_embeddings.pkl
        - Load the retrieval results from the outputs/task_9_retrieval_results.json
        - Combine the user query with the 3 most similar chunks and the 3 most different chunks
        - Generate an improved answer using the LLM
        - Save the improved answer to the outputs/task_10.txt
        - Provide structured output where each insight has a justification and citation (source file)
        - Evaluate recall using the same LLM-driven evaluation prompt from Task 6
    """

    import json
    from pathlib import Path

    from helpers import LlmModel

    query_path = Path("outputs/task_4_groundtruth.json")
    retrieval_path = Path("outputs/task_9_retrieval_results.json")
    prediction_path = Path("outputs/task_10_prediction.json")
    evaluation_path = Path("outputs/task_10_evaluation_report.json")

    if not query_path.exists():
        raise FileNotFoundError("Task 4 ground truth is missing; run task_4 first.")
    if not retrieval_path.exists():
        raise FileNotFoundError(
            "Task 9 retrieval results are missing; run task_9 first."
        )

    with open(query_path) as query_file:
        query_payload = json.load(query_file)
    query_text = query_payload.get("user_query", "").strip()
    groundtruth = query_payload.get("groundtruth_answers", [])

    with open(retrieval_path) as retrieval_file:
        retrieval = json.load(retrieval_file)

    nearest = retrieval.get("nearest_chunks", [])[:3]
    furthest = retrieval.get("furthest_chunks", [])[:3]

    context_entries = []
    for entry in nearest + furthest:
        chunk = entry["chunk"]
        context_entries.append(
            f"{chunk['chunk_id']} ({chunk.get('source_file', 'unknown')}): {chunk['text']}"
        )

    prompt = f"""
    You are an analyst answering a research question based on retrieved evidence.
    Generate at least three insights about the user query. Each insight must include a justification and a citation referencing the source file or chunk where the evidence came from.

    User query:
    {query_text}

    Retrieved chunks:
    {"".join(f"- {item}\\n" for item in context_entries)}

    Return the output as JSON with the format:
    {{
        "insights": [
            {{
                "insight": "<answer>",
                "justification": "<why this is true using the chunk text>",
                "citation": "<source file or chunk_id>"
            }}
        ]
    }}
    """

    llm = LlmModel()
    structured_response = llm.prompt_llm(prompt, get_structured_output="json")
    predicted_insights = structured_response.get("insights", [])
    predicted_insights_list = [item.get("insight", "") for item in predicted_insights]

    evaluation_prompt = f"""
    You are an evaluator.
    User Query: {query_text}

    Ground Truth Answers:
    {json.dumps(groundtruth, indent=2)}

    Predicted Insights:
    {json.dumps(predicted_insights_list, indent=2)}

    Compare the predicted insights with the ground truth answers.
    Calculate the Recall score: (Number of correctly retrieved ground truth answers) / (Total number of ground truth answers).

    Provide a concise justification for the score.

    Return the output in JSON format:
    {{
        "recall_score": <float between 0 and 1>,
        "justification": "<string>"
    }}
    """
    evaluation_report = llm.prompt_llm(evaluation_prompt, get_structured_output="json")

    prediction_path.parent.mkdir(exist_ok=True)

    helpers.save_json(structured_response, prediction_path)
    helpers.save_json(evaluation_report, evaluation_path)
