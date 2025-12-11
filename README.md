# 🧠 Deep Research Agent Workshop
Build a full Deep Research Agent in 12 hands-on tasks.

## 🎯 Goal
By the end of this workshop, you will have a working Deep Research Agent web app with RAG, LLM-as-Judge, citation support, and follow up interactions.

<p align="center">
  <img src="data/app.png" alt="Deep Research Agent UI Screenshot" width="100%">
</p>

## Installation
- `pip install -r requirements.txt`
- create `.env` with the together api key 

## ✅ Tasks

### Task 1: Python Setup and Hello World in Cursor
**Goal:** Ensure the environment is set up correctly and you can run Python code.
**Instructions:**
- Install Python and dependencies.
- Run a script that generates a very cool looking hello world message.
- Save the output to `outputs/task_1.txt`.

### Task 2: Basic LLM Prompting
**Goal:** Send an interesting prompt to an LLM and capture the response.
**Instructions:**
- Send an interesting prompt to an LLM.
- Print and save the model response to `outputs/task_2.txt`.

### Task 3: Structured LLM Prompting
**Goal:** Provide a passage and extract three justified insights via a structured prompt.
**Instructions:**
- Load the data from `data/christmas.txt`.
- Provide three insights about the passage, each paired with a justification.
- Return JSON with a `passage` key (the text) and an `insights` list where each object has `insight` and `justification`.
- Save the structured output (nicely formatted markdown) to `outputs/task_3.txt`.

### Task 4: Create a User Query and Evidence
**Goal:** Create a ground-truth user query plus three evidence answers that support it.
**Instructions:**
- Define a user query from a meaningful domain (e.g., healthcare, finance, university, energy).
- Write three direct, quantitative ground-truth answers that lead to the query’s resolution.
- Persist the ground-truth to `outputs/task_4_groundtruth.txt`.

### Task 5: Create the Needle in the Haystack Text File
**Goal:** Turn the ground-truth into a single knowledge-base file.
**Instructions:**
- Load the ground-truth from `outputs/task_4_groundtruth.json`.
- Insert the `groundtruth_answers` into a single text file containing the user query and answers.
- Save the result to `outputs/task_5_needle_in_haystack.txt`.

### Task 6: Evaluate the Recall of the Insight Extraction using LLM-as-a-Judge (Predict and Evaluate)
**Goal:** Measure recall of the candidate insights using LLM-as-a-judge.
**Instructions:**
- Load the user query and ground-truth answers from `outputs/task_4_groundtruth.json`.
- Load the predicted insights from `outputs/task_5_insights.json`.
- Evaluate recall by comparing the predicted insights to the ground-truth answers.
- Save the evaluation report to `outputs/task_6_evaluation_report.json`.

### Task 7: Create Three Needle-in-Haystack Files
**Goal:** Produce one target knowledge file and two distractors.
**Instructions:**
- Create two distractor files by loading the passage from `outputs/task_5_needle_in_haystack.txt`.
- Create one target file from the same passage (only file 1 should be the target, others distractors).
- Save the files as `outputs/task_7_file_1.txt`, `outputs/task_7_file_2.txt`, and `outputs/task_7_file_3.txt`.

### Task 8: Chunk and Embed All Files
**Goal:** Chunk the three haystack files, embed every chunk, and persist the data for retrieval.
**Instructions:**
- Load the three files from `outputs/task_7_file_1.txt`, `outputs/task_7_file_2.txt`, and `outputs/task_7_file_3.txt`.
- Chunk them into 64-token pieces with a 12-token overlap.
- Embed each chunk using Sentence Transformers.
- Save the chunks and embeddings to `outputs/task_8_chunks.json` and `outputs/task_8_embeddings.pkl`.

### Task 9: Build the Retrieval System
**Goal:** Retrieve the closest and most different chunks for a query and log their scores.
**Instructions:**
- Load the user query from `outputs/task_4_groundtruth.json`.
- Load the chunk metadata and embeddings produced in Task 8.
- Embed the query, score every chunk, and print the top three closest chunks.
- Save the query plus the nearest and most different chunks (with metadata) to `outputs/task_9_retrieval_results.json`.

### Task 10: Augmented Generation Stage Two of RAG
**Goal:** Combine retrieved chunks with the query to generate an improved answer with citations and recall evaluation.
**Instructions:**
- Load the user query from `outputs/task_4_groundtruth.json`.
- Load chunks and embeddings from `outputs/task_8_chunks.json` and `outputs/task_8_embeddings.pkl`.
- Load retrieval results from `outputs/task_9_retrieval_results.json`.
- Combine the user query with the three most similar and three most different chunks.
- Generate an improved answer using the LLM.
- Save the structured answer to `outputs/task_10.txt`, ensuring each insight has a justification and file citation.
- Evaluate recall using the same LLM-driven evaluation prompt from Task 6.

### Task 11: Build a Flask Deep Research App with Citations
**Goal:** Launch a Flask app that accepts queries and returns cited insights.
**Instructions:**
- Create a Flask app with a query endpoint that returns insights and citations derived from the three files.
- Reuse RAG logic from Tasks 8, 9, and 10 (via helper functions if helpful).
- Save the outputs to `outputs/task_11.json`.

### Task 12: Add Follow Up Question Support
**Goal:** Make the Flask app notebook-style so users can issue follow-ups after seeing insights.
**Instructions:**
- Create a Flask app endpoint that returns insights and citations for a user query, then lets the user ask a follow-up that reruns the retrieval pipeline.
- Reuse the RAG stack from Tasks 8, 9, and 10.
- Ensure the search bar reappears each time the user sees insights and citations.
- Save the outputs to `outputs/task_12.json`.

### Final Challenge
* Make a beautiful looking Deep Research App where the user can select the folder where the files are.
* Most beautiful site will get an award from me, just send the code and screenshot to the "outputs" discord channel

## 🧩 Final Output
A complete Deep Research Agent that retrieves information across multiple files, generates structured insights, cites exact sources, evaluates recall, serves results through a Flask API, and handles follow up interactions.

**About the Teacher:**
​Issam Laradji is a Research Scientist at ServiceNow and an Adjunct Professor at University of British Columbia. He holds a PhD in Computer Science and a PhD from the University of British Columbia, and his research interests include natural language processing, computer vision, and large-scale optimization.

Feel free to connect on LinkedIn: https://www.linkedin.com/in/issam-laradji-67ba1a99/