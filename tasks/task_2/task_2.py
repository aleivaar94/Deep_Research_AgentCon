import os
import helpers


def task_2():
    """
    Goal:
        Send an interesting prompt to an LLM and print the model response.
    Instructions:
        - Send an interesting prompt to an LLM
        - Print & save the model response to outputs/task_2.txt
    """
    prompt = (
        "Generate a cool and short message about how AI is transforming the future."
    )

    llm = helpers.LlmModel()
    response = llm.prompt_llm(prompt)

    print("Model Response:")
    print(response)

    helpers.save_txt(response, "outputs/task_2.txt")
