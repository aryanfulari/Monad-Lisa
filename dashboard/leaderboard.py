"""
leaderboard.py — Feature: Model Leaderboard

Reads on-chain achievements via blockchain.blockchain.get_achievements() and
aggregates average score per model, based on the "[{model}] {task}" tag
written by pipeline.py's tag_task().

IMPORTANT — matches the REAL contract struct order confirmed from blockchain.py:
    Achievement(task, score, feedback, timestamp)
get_achievements() returns a list of these as tuples (or tuple-like structs),
so we index by position: a[0]=task, a[1]=score, a[2]=feedback, a[3]=timestamp.
(Same indexing get_stats() already relies on with a[1].)

Achievements written BEFORE this feature existed won't have a tag — those are
bucketed under "untagged" rather than dropped, so old demo history still shows
up somewhere instead of silently disappearing.
"""

import re
from collections import defaultdict

TAG_PATTERN = re.compile(r"^\[([^\[\]]+)\]\s?(.*)$")


def parse_model_tag(task: str):
    """Returns (model_name, original_task) if tagged, else (None, task)."""
    match = TAG_PATTERN.match(task)
    if match:
        return match.group(1), match.group(2)
    return None, task


def get_leaderboard(agent_address: str, get_achievements_fn=None):
    """
    Returns:
    {
        "gemini-2.5-flash": {"count": 5, "avg_score": 91.4},
        "untagged": {"count": 2, "avg_score": 75.0},
        ...
    }
    """
    if get_achievements_fn is None:
        from blockchain.blockchain import get_achievements as get_achievements_fn

    achievements = get_achievements_fn(agent_address)

    buckets = defaultdict(list)
    for a in achievements:
        task = a[0]
        score = a[1]
        model, _ = parse_model_tag(task)
        buckets[model or "untagged"].append(score)

    return {
        model: {"count": len(scores), "avg_score": round(sum(scores) / len(scores), 1)}
        for model, scores in buckets.items()
    }


def get_leaderboard_sorted(agent_address: str, get_achievements_fn=None):
    """Same data, sorted desc by avg_score — ready to feed a bar chart in app.py."""
    board = get_leaderboard(agent_address, get_achievements_fn)
    return sorted(board.items(), key=lambda kv: kv[1]["avg_score"], reverse=True)
