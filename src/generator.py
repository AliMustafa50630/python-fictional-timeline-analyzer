"""
generator.py
Creates fictional characters, locations, and events for the Alibi Engine.
All data produced here is synthetic and used only for practicing Python logic.
"""

import random
import json
from datetime import datetime, timedelta

TIME_FORMAT = "%Y-%m-%d %H:%M"
FIRST_NAMES = [
    "Ali", "Ahmed", "Hamza", "Usman",
    "Ayesha", "Hira", "Zainab", "Sara"
]

LAST_NAMES = [
    "Khan", "Malik", "Qureshi", "Ahmed",
    "Raza", "Sheikh", "Siddiqui", "Abbasi"
]

LOCATIONS = [
    "Gulberg Cafe",
    "Quaid-e-Azam Library",
    "Packages Mall",
    "Liberty Market",
    "Model Town Park",
    "Johar Town",
    "Lahore Railway Station",
    "Fortress Square"
]

ACTIVITIES = [
    "Meeting a friend",
    "Studying at the library",
    "Watching a movie",
    "Shopping",
    "Spending time at home",
    "Taking a walk",
    "Waiting for a train",
    "Having dinner"
]

def generate_character_name(used_names):
    """Generate a unique fictional character name."""
    while True:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if name not in used_names:
            used_names.add(name)
            return name


def generate_case(case_name="Fictional Case File", num_characters=3,
                   min_events=4, max_events=6, seed=None):
    """Build a complete fictional case with characters and their events."""
    if seed is not None:
        random.seed(seed)

    used_names = set()
    characters = [generate_character_name(used_names) for _ in range(num_characters)]

    events = []
    event_id = 1
    base_date = datetime(2025, 6, 14)

    for character in characters:
        num_events = random.randint(min_events, max_events)
        current_time = base_date + timedelta(
            hours=random.randint(6, 9),
            minutes=random.choice([0, 15, 30, 45]),
        )

        for _ in range(num_events):
            location = random.choice(LOCATIONS)
            activity = random.choice(ACTIVITIES)
            duration_minutes = random.randint(30, 150)

            start_time = current_time
            end_time = start_time + timedelta(minutes=duration_minutes)

            events.append({
                "event_id": event_id,
                "character": character,
                "location": location,
                "activity": activity,
                "start_time": start_time.strftime(TIME_FORMAT),
                "end_time": end_time.strftime(TIME_FORMAT),
            })
            event_id += 1

            # A random (sometimes negative) gap is left before the next event.
            # Negative or very small gaps naturally create overlaps and tight
            # travel windows, which is exactly what the timeline engine
            # is meant to detect.
            gap_minutes = random.randint(-20, 90)
            current_time = end_time + timedelta(minutes=gap_minutes)

    case = {
        "case_name": case_name,
        "generated_on": datetime.now().strftime(TIME_FORMAT),
        "characters": characters,
        "locations": LOCATIONS,
        "events": events,
    }
    return case


def save_case(case, filepath):
    """Save a case dictionary to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(case, file, indent=4)
        return True
    except OSError as error:
        print(f"Error saving case file: {error}")
        return False


def load_case(filepath):
    """Load a case dictionary from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Case file not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Case file is not valid JSON: {filepath}")
        return None
