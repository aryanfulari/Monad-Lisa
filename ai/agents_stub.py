import random

def worker_agent(task: str, model: str = "stub-model") -> str:
    return f"[stub output ({model}) for task: {task[:40]}]"

def judge_agent(task: str, output: str, model: str = "stub-model") -> dict:
    return {"score": random.randint(70, 95), "feedback": "Stub feedback — solid attempt on this task."}