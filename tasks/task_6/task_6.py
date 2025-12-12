import helpers
import json
import os
from together import Together
from dotenv import load_dotenv


def task_6(mode="evaluate"):
    """
    Goal:
        Evaluate the Recall of the Insight extraction using LLM-as-a-Judge (Predict and Evaluate)
    Instructions:
        - Load the user query from the file outputs/task_4_groundtruth.json
        - Load the groundtruth answers from the file outputs/task_4_groundtruth.json
        - Load the predicted insights from the file outputs/task_5_insights.json
        - Evaluate the recall of the predicted insights using the groundtruth answers
        - Save the evaluation report to the file outputs/task_6_evaluation_report.json
    """
    load_dotenv()
    
    if mode == "predict":
        # Load user query
        try:
            with open("outputs/task_4_groundtruth.json", "r") as f:
                groundtruth = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            groundtruth = {
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
        
        user_query = groundtruth["user_query"]
        
        # Load the needle file
        needle_content = helpers.load_txt("outputs/task_5_needle_in_haystack.txt")
        
        # Use LLM to extract insights
        prompt = f"""
Based on the following knowledge base content, extract key insights that directly answer the user query: "{user_query}"

Knowledge Base:
{needle_content}

Provide a list of insights that are direct, quantitative, and relevant to the query. Return ONLY a valid JSON array of strings, each being a concise insight. Do not include any additional text, explanations, or formatting.
"""
        
        try:
            client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3.1",
                messages=[{"role": "user", "content": prompt}]
            )
            predicted_insights = json.loads(response.choices[0].message.content)
            
            # Save predicted insights
            with open("outputs/task_5_insights.json", "w") as f:
                json.dump(predicted_insights, f, indent=4)
        except Exception as e:
            print(f"Error in predict mode: {e}")
    
    elif mode == "evaluate":
        # Load groundtruth
        try:
            with open("outputs/task_4_groundtruth.json", "r") as f:
                groundtruth = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            groundtruth = {
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
        
        groundtruth_answers = groundtruth["groundtruth_answers"]
        
        # Load predicted insights
        try:
            with open("outputs/task_5_insights.json", "r") as f:
                predicted_insights = json.load(f)
        except FileNotFoundError:
            print("Predicted insights file not found. Run predict mode first.")
            return
        
        # Use LLM to evaluate recall
        prompt = f"""
Evaluate the recall of the predicted insights compared to the groundtruth answers.

Groundtruth Answers:
{json.dumps(groundtruth_answers, indent=2)}

Predicted Insights:
{json.dumps(predicted_insights, indent=2)}

For each groundtruth answer, determine if it is adequately covered by the predicted insights. Provide a score from 0 to 1 for each, where 1 means fully covered, 0 means not covered.

Then, calculate the overall recall as the average score.

Return ONLY a valid JSON object with:
- "individual_scores": a list of scores for each groundtruth answer
- "overall_recall": the average score
- "reasoning": a brief explanation

Do not include any additional text.
"""
        
        try:
            client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3.1",
                messages=[{"role": "user", "content": prompt}]
            )
            evaluation = json.loads(response.choices[0].message.content)
            
            # Save evaluation report
            with open("outputs/task_6_evaluation_report.json", "w") as f:
                json.dump(evaluation, f, indent=4)
        except Exception as e:
            print(f"Error in evaluate mode: {e}")
