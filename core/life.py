from core.goals import GOALS
from core.memory import add_to_memory
from core.state import STATE
import random

def pick_daily_goal():
    return random.choice(GOALS)

def simulate_emotion(outcome):
    if outcome == "success":
        STATE["mood"] = "euforico"
        STATE["motivation"] += 10
        STATE["energy"] -= 5
    elif outcome == "failure":
        STATE["mood"] = "frustrato"
        STATE["motivation"] -= 15
        STATE["energy"] -= 10
    else:
        STATE["mood"] = "neutrale"

    # clamp
    STATE["motivation"] = max(0, min(100, STATE["motivation"]))
    STATE["energy"] = max(0, min(100, STATE["energy"]))

def simulate_task():
    goal = pick_daily_goal()
    print(f"\n🛠 Invader decide di lavorare su: '{goal}'")

    # casual outcome
    outcome = random.choice(["success", "failure", "neutral"])
    STATE["last_outcome"] = outcome
    simulate_emotion(outcome)

    # log memory
    add_to_memory({
        "event": "daily_task",
        "goal": goal,
        "outcome": outcome,
        "mood": STATE["mood"],
        "motivation": STATE["motivation"],
        "energy": STATE["energy"]
    })

    return goal, outcome 