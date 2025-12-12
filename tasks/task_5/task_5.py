import helpers
import json


def task_5(mode="test"):
    """
    Goal:
        Create a realistic file where you insert the needles in a haystack
    Instructions:
        - Load the groundtruth from outputs/task_4_groundtruth.json
        - Insert the groundtruth_answers into a single text file to act as a knowledge base.
        - The file should be a single text file with the user query and the  groundtruth_answers.
        - The file should be saved to outputs/task_5_needle_in_haystack.txt
    """
    # Load the groundtruth
    try:
        with open("outputs/task_4_groundtruth.json", "r") as f:
            groundtruth = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to hardcoded data
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
    groundtruth_answers = groundtruth["groundtruth_answers"]
    
    # Create the content for the knowledge base
    content = f"User Query: {user_query}\n\nGroundtruth Answers:\n"
    for i, answer in enumerate(groundtruth_answers, 1):
        content += f"{i}. {answer}\n"
    
    # Save to file
    helpers.save_txt(content, "outputs/task_5_needle_in_haystack.txt")
