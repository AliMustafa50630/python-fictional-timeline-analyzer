"""
report.py
Calculates a transparent, rule-based consistency score and builds the
final readable report for a fictional case.
"""

# Points subtracted from a perfect score of 100 for each conflict type.
PENALTY_POINTS = {
    "Impossible Presence": 25,
    "Duplicate Booking": 10,
    "Insufficient Travel Time": 8,
}


def calculate_consistency_score(conflicts):
    """Calculate a simple rule-based consistency score from 0 to 100."""
    score = 100
    for conflict in conflicts:
        penalty = PENALTY_POINTS.get(conflict["conflict_type"], 5)
        score -= penalty
    return max(score, 0)


def score_label(score):
    """Translate a numeric score into a plain-English verdict."""
    if score >= 90:
        return "Highly Consistent"
    elif score >= 70:
        return "Mostly Consistent"
    elif score >= 50:
        return "Questionable"
    else:
        return "Highly Inconsistent"


def format_conflict(conflict):
    """Return a human-readable description of a single conflict."""
    event_1 = conflict["event_1"]
    event_2 = conflict["event_2"]
    lines = [
        f"  [{conflict['conflict_type']}] {conflict['character']}",
        f"    - {event_1['start_time']} to {event_1['end_time']} at {event_1['location']} ({event_1['activity']})",
        f"    - {event_2['start_time']} to {event_2['end_time']} at {event_2['location']} ({event_2['activity']})",
    ]
    if "gap_minutes" in conflict:
        lines.append(f"    - Only {conflict['gap_minutes']} minutes available to travel")
    return "\n".join(lines)


def generate_report(case, conflicts):
    """Build the full text report for a case."""
    score = calculate_consistency_score(conflicts)
    label = score_label(score)

    lines = []
    lines.append("=" * 60)
    lines.append(f"ALIBI ENGINE REPORT - {case['case_name']}")
    lines.append("=" * 60)
    lines.append(f"Generated on: {case.get('generated_on', 'unknown')}")
    lines.append(f"Characters involved: {', '.join(case['characters'])}")
    lines.append(f"Total events recorded: {len(case['events'])}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("CONFLICTS DETECTED")
    lines.append("-" * 60)
    if conflicts:
        for conflict in conflicts:
            lines.append(format_conflict(conflict))
            lines.append("")
    else:
        lines.append("  No conflicts detected. All timelines are consistent.")
        lines.append("")

    lines.append("-" * 60)
    lines.append("CONSISTENCY SCORE")
    lines.append("-" * 60)
    lines.append(f"  Score: {score}/100")
    lines.append(f"  Verdict: {label}")
    lines.append("=" * 60)

    return "\n".join(lines)


def save_report(report_text, filepath):
    """Save the report text to a file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(report_text)
        return True
    except OSError as error:
        print(f"Error saving report: {error}")
        return False
