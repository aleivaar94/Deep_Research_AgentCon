import helpers
import flask, together, textwrap, json, os, sys, argparse
import dotenv

dotenv.load_dotenv()


def task_1():
    """
    Goal:
      Ensure the environment is set up correctly and you can run Python code.

    Instructions:
    - Install Python and dependencies
    - Run a script that generates a very cool looking hello world message
    - Save the output to outputs/task_1.txt.
    """
    text = "hello world"
    print(text)

    helpers.save_txt(text, "outputs/task_1.txt")
