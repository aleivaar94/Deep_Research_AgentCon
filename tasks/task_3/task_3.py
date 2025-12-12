import json
import os
import helpers
from together import Together
from dotenv import load_dotenv


def task_3():
    """
    Goal:
        Provide a paragraph and extract three insights with justifications using a structured prompt.

    Instructions:
        - Load the data from data/christmas.txt
        - Provide 3 insights about the passage as a list, where each insight includes a justification.
        - Return the response in JSON format with two keys: 'passage' (containing the text) and 'insights' (a list of objects with 'insight' and 'justification' keys).
        - Save the structured output nicely (in markdown format) to outputs/task_3.txt.
    """
    load_dotenv()
    
    # Load the passage
    passage = helpers.load_txt("data/christmas.txt")
    
    prompt = f"""
Analyze the following passage about Christmas celebrations and extract exactly 3 key insights. For each insight, provide a brief justification based on the text.

Passage:
{passage}

Return ONLY a valid JSON object with two keys:
- 'passage': the full text of the passage
- 'insights': a list of exactly 3 objects, each with 'insight' and 'justification' keys.

For example:
        The response should be in the following format:
        {{
            "insights": [
                {{
                    "insight": "The groundtruth answer",
                    "justification": "The justification for the answer"
                }}
            ]
        }}

Do not include any additional text, explanations, or formatting outside the JSON.
"""
    
    try:
        client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.1",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        response_content = response.choices[0].message.content
        
        # Parse the JSON response
        result = json.loads(response_content)
        
        helpers.save_txt(json.dumps(result, indent=4), "outputs/task_3.txt")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to process the task.")
