from datetime import datetime

from blockchain.blockchain import get_achievements


def get_dashboard_data(agent_address: str) -> dict:
    achievements = get_achievements(agent_address)

    if not achievements:
        return {
            "agent_id": agent_address,
            "status": "New Agent",
            "tasks_completed": 0,
            "average_score": 0,
            "highest_score": 0,
            "last_activity": "No activity",
            "trust_score": 0,
            "level": "Beginner",
        }

    scores = [item[1] for item in achievements]

    latest_timestamp = max(item[3] for item in achievements)

    last_activity = datetime.fromtimestamp(
        latest_timestamp
    ).strftime("%d %b %Y %I:%M %p")

    average = round(sum(scores) / len(scores), 1)

    trust_score = round(min(100, average + len(scores) * 0.5), 1)

    if average >= 95:
        level = "Elite"
    elif average >= 90:
        level = "Expert"
    elif average >= 80:
        level = "Advanced"
    elif average >= 70:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {
        "agent_id": agent_address,
        "status": "Verified",
        "tasks_completed": len(achievements),
        "average_score": average,
        "highest_score": max(scores),
        "last_activity": last_activity,
        "trust_score": trust_score,
        "level": level,
    }


def get_badges(agent_address: str) -> list[dict]:

    achievements = get_achievements(agent_address)

    scores = [a[1] for a in achievements]

    average = sum(scores) / len(scores) if scores else 0

    return [

        {
            "name": "First Task",
            "icon": "🏅",
            "earned": len(achievements) >= 1,
        },

        {
            "name": "5 Tasks",
            "icon": "🔥",
            "earned": len(achievements) >= 5,
        },

        {
            "name": "10 Tasks",
            "icon": "🚀",
            "earned": len(achievements) >= 10,
        },

        {
            "name": "Perfect Score",
            "icon": "💯",
            "earned": any(score == 100 for score in scores),
        },

        {
            "name": "High Performer",
            "icon": "⭐",
            "earned": average >= 90,
        },

    ]


def get_performance_history(agent_address: str):

    achievements = get_achievements(agent_address)

    history = []

    for task, score, feedback, timestamp in reversed(achievements):

        history.append({

            "Task": task,

            "Score": score,

            "Date": datetime.fromtimestamp(
                timestamp
            ).strftime("%d %b %Y"),

            "Time": datetime.fromtimestamp(
                timestamp
            ).strftime("%I:%M %p"),

            "Feedback": feedback,

        })

    return history