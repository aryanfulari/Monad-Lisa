"""
Zero-cost wiring test — no real Gemini calls, no real chain writes.
Fake achievements match the REAL contract struct order confirmed in
blockchain.py: (task, score, feedback, timestamp) — same indexing get_stats()
already uses (a[1] for score).
"""

from pipeline import tag_task
from leaderboard import get_leaderboard, get_leaderboard_sorted, parse_model_tag


def fake_get_achievements(agent_address):
    return [
        (tag_task("Dijkstra's algorithm", "gemini-2.5-flash"), 98, "Clean and correct.", 1751000000),
        (tag_task("Japan capital", "gemini-2.5-flash"), 100, "Perfect.", 1751000100),
        (tag_task("AI words", "gemini-3.5-flash"), 96, "Good, minor gaps.", 1751000200),
        (tag_task("AI words", "gemini-3.5-flash"), 94, "Solid.", 1751000300),
        (tag_task("German translations", "gemini-2.5-flash-lite"), 78, "Some errors.", 1751000400),
        ("German translations", 90, "Pre-tag legacy entry.", 1750000000),  # untagged (pre-feature)
    ]


def run():
    tagged = tag_task("Dijkstra's algorithm", "gemini-2.5-flash")
    assert tagged == "[gemini-2.5-flash] Dijkstra's algorithm"

    model, task = parse_model_tag(tagged)
    assert model == "gemini-2.5-flash" and task == "Dijkstra's algorithm"

    weird = tag_task("Explain [Big-O] notation", "gemini-2.5-flash")
    m2, t2 = parse_model_tag(weird)
    assert m2 == "gemini-2.5-flash" and t2 == "Explain [Big-O] notation"

    print("--- get_leaderboard() ---")
    board = get_leaderboard("0xFake", get_achievements_fn=fake_get_achievements)
    for model, stats in board.items():
        print(f"{model:>22}: count={stats['count']:<2} avg_score={stats['avg_score']}")

    print("\n--- get_leaderboard_sorted() ---")
    for model, stats in get_leaderboard_sorted("0xFake", get_achievements_fn=fake_get_achievements):
        print(f"{model:>22}: {stats['avg_score']}")

    print("\nAll checks passed.")


if __name__ == "__main__":
    run()
