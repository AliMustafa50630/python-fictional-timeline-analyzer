"""
timeline.py
Builds chronological timelines and detects conflicts between fictional events.
"""

from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_time(time_str):
    """Convert a stored time string into a datetime object."""
    return datetime.strptime(time_str, TIME_FORMAT)


def get_character_events(case, character):
    """Return all events for one character, sorted by start time."""
    character_events = [event for event in case["events"] if event["character"] == character]
    character_events.sort(key=lambda event: parse_time(event["start_time"]))
    return character_events


def build_full_timeline(case):
    """Return a dictionary mapping each character to their sorted events."""
    timeline = {}
    for character in case["characters"]:
        timeline[character] = get_character_events(case, character)
    return timeline


def events_overlap(event_a, event_b):
    """Return True if two events share any overlapping time range."""
    start_a = parse_time(event_a["start_time"])
    end_a = parse_time(event_a["end_time"])
    start_b = parse_time(event_b["start_time"])
    end_b = parse_time(event_b["end_time"])
    return start_a < end_b and start_b < end_a


def detect_overlap_conflicts(case):
    """Find events belonging to the same character that overlap in time."""
    conflicts = []
    timeline = build_full_timeline(case)

    for character, events in timeline.items():
        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                event_a = events[i]
                event_b = events[j]
                if events_overlap(event_a, event_b):
                    if event_a["location"] != event_b["location"]:
                        conflict_type = "Impossible Presence"
                    else:
                        conflict_type = "Duplicate Booking"
                    conflicts.append({
                        "conflict_type": conflict_type,
                        "character": character,
                        "event_1": event_a,
                        "event_2": event_b,
                    })
    return conflicts


def detect_travel_conflicts(case, min_travel_minutes=15):
    """Find consecutive events at different locations with too little travel time."""
    conflicts = []
    timeline = build_full_timeline(case)

    for character, events in timeline.items():
        for i in range(len(events) - 1):
            current_event = events[i]
            next_event = events[i + 1]

            if events_overlap(current_event, next_event):
                continue  # already reported as an overlap conflict

            gap = parse_time(next_event["start_time"]) - parse_time(current_event["end_time"])
            gap_minutes = gap.total_seconds() / 60

            if (current_event["location"] != next_event["location"]
                    and 0 <= gap_minutes < min_travel_minutes):
                conflicts.append({
                    "conflict_type": "Insufficient Travel Time",
                    "character": character,
                    "event_1": current_event,
                    "event_2": next_event,
                    "gap_minutes": round(gap_minutes, 1),
                })
    return conflicts


def analyze_case(case, min_travel_minutes=15):
    """Run all conflict checks and return one combined list of conflicts."""
    conflicts = []
    conflicts.extend(detect_overlap_conflicts(case))
    conflicts.extend(detect_travel_conflicts(case, min_travel_minutes))
    return conflicts
