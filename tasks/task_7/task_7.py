import helpers


def task_7():
    """
    Goal:
        Create Three Needle-in-Haystack files (two of them are distractor files, and one is the target file from task 5)
    Instructions:
        - Create two distractor files by loading the passage from the file outputs/task_5_needle_in_haystack.txt
        - Create one target file by loading the passage from the file outputs/task_5_needle_in_haystack.txt
        - only file 1 is the target file, the other two are distractor files
        - Save the three files to the outputs/task_7_file_1.txt, outputs/task_7_file_2.txt, and outputs/task_7_file_3.txt
    """
    base_passage = helpers.load_txt("outputs/task_5_needle_in_haystack.txt")
    helpers.save_txt(base_passage, "outputs/task_7_file_1.txt")

    try:
        llm = helpers.LlmModel()
        distractor_one = _generate_distractor(llm, base_passage, "Apparel")
        distractor_two = _generate_distractor(llm, base_passage, "Home goods")
    except Exception as e:
        print(f"LLM generation failed: {e}. Using simple replacements.")
        distractor_one = base_passage.replace("Electronics", "Clothing")
        distractor_two = base_passage.replace("Electronics", "Books")

    helpers.save_txt(distractor_one, "outputs/task_7_file_2.txt")
    helpers.save_txt(distractor_two, "outputs/task_7_file_3.txt")


def _generate_distractor(llm, base_passage, category_name):
    prompt = f"""
Take inspiration from the style of the passage below (three sections, bolded headings, narrative tone)
but create a completely new piece that focuses on {category_name}. Do not reuse the original facts,
metrics, or conclusions. 

Instead, weave a different storyline that could plausibly come from a
market analysis but is not directly relevant to the original question. Maintain the formatting cues
(bolded section titles, short paragraphs) so the file blends into the haystack.

Original passage for reference:
{base_passage}

Return only the new passage text you generate.
"""
    return llm.prompt_llm(prompt)