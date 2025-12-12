import helpers
import json


def task_4(mode="default"):
    """
    Goal:
        Create a groundtruth example of a user query and three groundtruth answers that lead to answering the query.
    Instructions:
        - Define a user query from a domain like healtcare, finance, university, energy, etc.
        - Write three groundtruth answers (need to be direct and quantitative) that lead to answering the query
        - These answers will serve as the ground truth for later steps
        - Save the output to outputs/task_4_groundtruth.txt
    """
    user_query = "What product type delivers the highest profit-per-customer during Christmas sales?"
    groundtruth_answers = [
        "Electronics show the highest 42 percent profit.",
        "Next category peaks at only 35 percent.",
        "Average category profit rises just 24 percent.",
        "Electronics exceed category average by 18 percent.",
        "Electronics beat runner-up category by 7 percent.",
        "Electronics generate 31 dollars more per customer.",
        "Electronics drive 14 percent greater holiday uplift.",
        "Electronics lead all segments in margin growth."
    ]
    
    data = {
        "user_query": user_query,
        "groundtruth_answers": groundtruth_answers
    }
    
    # Save as JSON to match task_5 expectation
    with open("outputs/task_4_groundtruth.json", "w") as f:
        json.dump(data, f, indent=4)
    
    # Also save as txt for the instruction
    content = f"User Query: {user_query}\n\nGroundtruth Answers:\n"
    for i, answer in enumerate(groundtruth_answers, 1):
        content += f"{i}. {answer}\n"
    helpers.save_txt(content, "outputs/task_4_groundtruth.txt")
