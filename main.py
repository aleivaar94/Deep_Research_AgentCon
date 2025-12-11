import argparse
import tasks

from dotenv import load_dotenv


load_dotenv()

TASK_LIST = [f"task_{i}" for i in range(1, 13)]

if __name__ == "__main__":
    # create a parser for the command line arguments
    # the parse only asks which task to run and then calls the main function
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        "-t",
        type=str,
        default="task_11",
        help="The task to run",
        choices=TASK_LIST,
    )
    args = parser.parse_args()

    # create an if and else statements there are 12 tasks
    if args.task == "task_1":
        # Task 1: Python Setup and Hello World in Cursor
        tasks.task_1.task_1()
    elif args.task == "task_2":
        # Task 2: Basic LLM Prompting
        tasks.task_2.task_2()
    elif args.task == "task_3":
        # Task 3: Structured LLM Prompting
        tasks.task_3.task_3()
    elif args.task == "task_4":
        # Task 4: Create a User Query and Evidence
        tasks.task_4.task_4()
    elif args.task == "task_5":
        # Task 5: Create the Needle in the Haystack Text File
        tasks.task_5.task_5()
    elif args.task == "task_6":
        # Task 6: Evaluate the Recall of the Insight extraction using LLM-as-a-Judge (Predict and Evaluate)
        tasks.task_6.task_6()
    elif args.task == "task_7":
        # Task 7: Create Three Needle-in-Haystack files (two of them are distractor files, and one is the target file from task 5)
        tasks.task_7.task_7()
    elif args.task == "task_8":
        # Task 8: Chunk and Embed All Files into a Vector Database
        tasks.task_8.task_8()
    elif args.task == "task_9":
        # Task 9: Build the Retrieval System
        tasks.task_9.task_9()
    elif args.task == "task_10":
        # Task 10: Augmented Generation Stage Two of RAG
        tasks.task_10.task_10()
    elif args.task == "task_11":
        # Task 11: Build a Flask Deep Research App with Citations
        tasks.task_11.task_11()
    elif args.task == "task_12":
        # Task 12: Add Follow Up Question Support
        tasks.task_12.task_12()
