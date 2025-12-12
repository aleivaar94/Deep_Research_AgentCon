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

    import os
    from together import Together
    from dotenv import load_dotenv

    load_dotenv()

    query_path = Path("outputs/task_4_groundtruth.json")
    retrieval_path = Path("outputs/task_9_retrieval_results.json")
    prediction_path = Path("outputs/task_10_prediction.json")
    evaluation_path = Path("outputs/task_10_evaluation_report.json")

    try:
        with open(query_path) as query_file:
            query_payload = json.load(query_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Task 4 ground truth not found or invalid; using fallback data.")
        query_payload = {
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
    query_text = query_payload.get("user_query", "").strip()
    groundtruth = query_payload.get("groundtruth_answers", [])

    try:
        with open(retrieval_path) as retrieval_file:
            retrieval = json.load(retrieval_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Task 9 retrieval results not found or invalid; cannot proceed.")
        return

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
    
    output only in raw json format that should be 1 valid dictionary, do not include any other text or comments.
    """

    try:
        client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.1",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.choices[0].message.content
        
        # Try to parse JSON
        try:
            structured_response = json.loads(output)
        except json.JSONDecodeError:
            # Extract JSON if wrapped in text
            import re
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                structured_response = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found in response")
        
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
        
        output only in raw json format that should be 1 valid dictionary, do not include any other text or comments.
        """
        
        eval_response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.1",
            messages=[{"role": "user", "content": evaluation_prompt}]
        )
        eval_output = eval_response.choices[0].message.content
        
        try:
            evaluation_report = json.loads(eval_output)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', eval_output, re.DOTALL)
            if json_match:
                evaluation_report = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found in eval response")
        
        evaluation_report["user_query"] = query_text
        structured_response["user_query"] = query_text
        prediction_path.parent.mkdir(exist_ok=True)

        helpers.save_json(structured_response, prediction_path)
        helpers.save_json(evaluation_report, evaluation_path)
        print("Saved task_10 files successfully.")
    except Exception as e:
        print(f"Error in task_10: {e}")
        print("Failed to generate or save outputs.")

