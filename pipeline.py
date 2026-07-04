from ai.agents import worker_agent, judge_agent
from blockchain.blockchain import record_achievement, account


# Feature: Model Tag On-Chain — no contract redeploy needed, pure string prefix.
# Format is locked as "[{model}] {task}" — leaderboard.py's parser depends on
# this exact format, so keep them in sync if this ever changes.
MODEL_TAG_FORMAT = "[{model}] {task}"


def tag_task(task: str, model: str) -> str:
    return MODEL_TAG_FORMAT.format(model=model, task=task)

def run_pipeline(task: str, model: str = "gemini-2.5-flash") -> dict:
    """
    Runs the complete AgentPassport pipeline.

    Flow:
    User Task
        ↓
    Worker Agent
        ↓
    Judge Agent
        ↓
    Record achievement on Monad
        ↓
    Return results
    """

    try:
        # Step 1: Generate AI response
        output = worker_agent(task, model= model)

        # Step 2: Judge the response
        result = judge_agent(task, output, model= model)

        score = result["score"]
        feedback = result["feedback"]

        # Step 3: Record achievement on blockchain
        # Step 3: Record achievement on blockchain
        tagged_task = tag_task(task, model)
        tx_hash = record_achievement(
            account.address,
            tagged_task,
            score,
            feedback
        )

        return {
            "success": True,
            "task": task,
            "output": output,
            "score": score,
            "feedback": feedback,
            "tx_hash": tx_hash,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":

    print("=" * 70)
    print("AgentPassport")
    print("=" * 70)

    task = input("\nEnter a task:\n> ")

    result = run_pipeline(task)

    if result["success"]:
        print("\n" + "=" * 70)
        print("WORKER OUTPUT")
        print("=" * 70)
        print(result["output"])

        print("\n" + "=" * 70)
        print("JUDGE RESULT")
        print("=" * 70)
        print(f"Score    : {result['score']}")
        print(f"Feedback : {result['feedback']}")

        print("\n" + "=" * 70)
        print("BLOCKCHAIN")
        print("=" * 70)
        print(f"Transaction Hash:\n{result['tx_hash']}")

    else:
        print("\nPipeline Error:")
        print(result["error"])