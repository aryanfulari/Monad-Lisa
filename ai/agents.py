from google import genai
from dotenv import load_dotenv
import os
import json
import re

# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"  

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# Worker Agent
# --------------------------------------------------

def worker_agent(task: str, model: str = DEFAULT_MODEL) -> str:
    """
    Executes any task using Gemini.
    """

    prompt = f"""
You are a highly capable AI assistant.

Your goal is to complete the user's task as accurately,
clearly and helpfully as possible.

Task:
{task}
"""

    try:

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        raise RuntimeError(f"Worker Agent Error: {e}")


# --------------------------------------------------
# Judge Agent
# --------------------------------------------------

def judge_agent(task: str, output: str, model: str = DEFAULT_MODEL) -> dict:
    """
    Evaluates the Worker's output.

    Returns:

    {
        "score": int,
        "feedback": str
    }
    """

    prompt = f"""
You are an impartial evaluator.

A Worker AI was given a task.

Your job is ONLY to evaluate how well it completed that task.

Original Task:
{task}

Worker Output:
{output}

Score the answer from 0 to 100.

Scoring Guidelines:

90-100
Excellent.
Completely satisfies the task.

70-89
Mostly correct with only minor issues.

40-69
Partially correct but missing important details.

0-39
Incorrect, irrelevant or poor quality.

Return ONLY valid JSON.

Example:

{{
    "score": 94,
    "feedback": "Accurate answer with good clarity."
}}
"""

    try:

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        text = response.text.strip()

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:
            raise ValueError("Judge did not return JSON.")

        data = json.loads(match.group(0))

        return {
            "score": int(data["score"]),
            "feedback": str(data["feedback"])
        }

    except Exception as e:

        return {
            "score": 0,
            "feedback": f"Judge Error: {e}"
        }


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    task = input("Enter a task:\n\n")

    print("\nRunning Worker Agent...\n")

    output = worker_agent(task)

    print("=" * 70)
    print("WORKER OUTPUT")
    print("=" * 70)
    print(output)

    print("\nRunning Judge Agent...\n")

    result = judge_agent(
        task,
        output
    )

    print("=" * 70)
    print("JUDGE RESULT")
    print("=" * 70)
    print(f"Score    : {result['score']}")
    print(f"Feedback : {result['feedback']}")