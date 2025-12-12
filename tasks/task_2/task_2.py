import os
import helpers
from together import Together
from dotenv import load_dotenv


def task_2():
    """
    Goal:
        Send an interesting prompt to an LLM and print the model response.
    Instructions:
        - Send an interesting prompt to an LLM
        - Print & save the model response to outputs/task_2.txt
    """
    load_dotenv()
    
    prompt = (
        "Generate a cool and short message about how AI is transforming the future."
    )

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
        
        print("Model Response:")
        print(response_content)
        
        helpers.save_txt(response_content, "outputs/task_2.txt")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to get response from LLM.")
