import helpers


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
    if mode == "default":
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
                "Electronics lead all segments in margin growth.",
            ],
        }

        helpers.save_json(groundtruth, "outputs/task_4_groundtruth.json")
    elif mode == "llm":
        # create a prompt_llm function that generates a user query and three groundtruth answers
        prompt = f"""
        Create a user query and three groundtruth answers that lead to answering the query.
        The user query should be a question from a domain like healtcare, finance, university, energy, etc.
        The groundtruth answers should be three direct and quantitative answers that lead to answering the query.
        Return the response in JSON format with two keys: 'user_query' and 'groundtruth_answers'.
        """
        llm = helpers.LlmModel()
        response = llm.prompt_llm(prompt, get_structured_output="json")
        user_query = response["user_query"]
        groundtruth_answers = response["groundtruth_answers"]
        groundtruth = {
            "user_query": user_query,
            "groundtruth_answers": groundtruth_answers,
        }

        helpers.save_json(groundtruth, "outputs/task_4_groundtruth_llm.json")
