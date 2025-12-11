# 🧠 Deep Research Agent Workshop
Build a full Deep Research Agent in 12 hands-on tasks.

## 🎯 Goal
By the end of this workshop, you will have a working Deep Research Agent web app with RAG, LLM-as-Judge, citation support, and follow up interactions.

## Installation
- `pip install -r requirements.txt`
- create `.env` with the together api key 

## ✅ Tasks

### Task 1: Python Setup and Hello World in Cursor
* Install Python and dependencies  
* Run a simple Hello World script in Cursor

### Task 2: Basic LLM Prompting
* Send a basic prompt to an LLM  
* Print the model response

### Task 3: Structured LLM Prompting
* Provide a paragraph  
* Extract three insights with justifications using a structured prompt

### Task 4: Create a User Query and Evidence
* Define a user query  
* Write three evidence answers that lead to answering the query

### Task 5: Create the Needle in the Haystack Text File
* Save the three evidence answers into a single text file  
* Use this file as the starting knowledge base

### Task 6: Evaluate the Recall of the Insight extraction using LLM-as-a-Judge (Predict and Evaluate)
* 

### Task 7: Create Three Needle-in-Haystack files (two of them are distractor files, and one is the target file from task 5)
* 

### Task 8: Chunk and Embed All Files
* Chunk the text across all three files  
* Create embeddings for every chunk  
* Store them in a vector database

### Task 9: Build the Retrieval System
* Retrieve the closest chunks to a user query  
* Print the retrieved chunks and similarity scores

### Task 10: Augmented Generation Stage Two of RAG
* Combine retrieved chunks with the user query  
* Generate an answer using the LLM with the chunks provided

### Task 11: Build a Flask Deep Research App with Citations
* Create a query endpoint  
* Return insights from the RAG pipeline  
* Add citations showing  
  * which file the insight came from  
  * which chunk number was used  
  * the original text snippet

### Task 12: Add Follow Up Question Support
* Generate follow up questions  
* Re query the system using the follow up  
* Refine insights based on additional context

## 🧩 Final Output
A complete Deep Research Agent that retrieves information across multiple files, generates structured insights, cites exact sources, evaluates recall, serves results through a Flask API, and handles follow up interactions.
