import json
import helpers


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
    # a 3 paragraph passage about how christmas is celebrated around the world
    christmas_passage = helpers.load_txt("data/christmas.txt")

    prompt = f"""
        Given the following passage: 
        {christmas_passage}
        Then, provide 3 insights about the passage as a list, where each insight includes a justification. 
        Return the response in JSON format with two keys: 'passage' (containing the text) and 'insights' 
        (a list of objects with 'insight' and 'justification' keys).
        
        Output the reponse in pure json format so that it can be extracted easily no other text or formatting.
    """

    llm = helpers.LlmModel()
    response = llm.prompt_llm(prompt, get_structured_output="json")

    print("Model Response:")
    print(json.dumps(response, indent=2))

    # Save as JSON formatted string to the text file
    helpers.save_json(response, "outputs/task_3.json")
