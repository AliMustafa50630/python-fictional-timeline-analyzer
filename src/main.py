"""
main.py
Command-line interface for the Alibi Engine timeline consistency simulator.

IMPORTANT: This is a fictional simulation project built for practicing
Python. It generates and analyzes made-up characters and events only.
It must not be used to create or support real-world alibis or deception.
"""

import os

from generator import generate_case, save_case, load_case
from timeline import build_full_timeline, analyze_case
from report import generate_report, save_report

# Resolve the data/ folder relative to this file, so it works from any
# directory the script is launched from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLE_CASE_PATH = os.path.join(DATA_DIR, "sample_case.json")
GENERATED_CASE_PATH = os.path.join(DATA_DIR, "generated_case.json")
REPORT_PATH = os.path.join(DATA_DIR, "last_report.txt")


def print_header():
    print("\n" + "=" * 50)
    print("      ALIBI ENGINE - Timeline Consistency Simulator")
    print("      (Fictional data only - for Python practice)")
    print("=" * 50)


def print_menu():
    print("\n1. Generate fictional case")
    print("2. Analyze existing case")
    print("3. Display timeline")
    print("4. Check conflicts")
    print("5. Generate report")
    print("6. Exit")


def display_timeline(case):
    """Print every character's events in chronological order."""
    timeline = build_full_timeline(case)
    print(f"\nTimeline for case: {case['case_name']}")

    for character, events in timeline.items():
        print(f"\n{character}")
        print("-" * len(character))
        if not events:
            print("  No events recorded.")
            continue
        for event in events:
            print(f"  {event['start_time']} - {event['end_time']} | "
                  f"{event['location']} | {event['activity']}")


def display_conflicts(case):
    """Print any detected conflicts for the current case."""
    conflicts = analyze_case(case)
    print(f"\nConflict check for case: {case['case_name']}")

    if not conflicts:
        print("  No conflicts detected. Timeline looks consistent.")
        return conflicts

    print(f"  {len(conflicts)} conflict(s) detected:\n")
    for conflict in conflicts:
        event_1 = conflict["event_1"]
        event_2 = conflict["event_2"]
        print(f"  [{conflict['conflict_type']}] {conflict['character']}")
        print(f"    - {event_1['start_time']} to {event_1['end_time']} at {event_1['location']}")
        print(f"    - {event_2['start_time']} to {event_2['end_time']} at {event_2['location']}")
    return conflicts


def handle_generate_case():
    """Ask the user for basic settings and generate a new fictional case."""
    try:
        raw_input_value = input("How many characters? (default 3): ").strip()
        num_characters = int(raw_input_value) if raw_input_value else 3
    except ValueError:
        print("Invalid number entered, using default of 3.")
        num_characters = 3

    case = generate_case(case_name="Randomly Generated Case", num_characters=num_characters)

    os.makedirs(DATA_DIR, exist_ok=True)
    if save_case(case, GENERATED_CASE_PATH):
        print(f"New case generated and saved to: {GENERATED_CASE_PATH}")

    return case


def handle_load_case():
    """Load a case from disk, defaulting to the bundled sample case."""
    path = input("Enter case file path (leave blank for sample case): ").strip()
    if not path:
        path = SAMPLE_CASE_PATH

    case = load_case(path)
    if case:
        print(f"Loaded case: {case['case_name']}")
    return case


def handle_generate_report(case):
    """Analyze the current case and print/save a full report."""
    conflicts = analyze_case(case)
    report_text = generate_report(case, conflicts)
    print("\n" + report_text)

    os.makedirs(DATA_DIR, exist_ok=True)
    if save_report(report_text, REPORT_PATH):
        print(f"\nReport saved to: {REPORT_PATH}")


def main():
    print_header()
    current_case = None

    while True:
        print_menu()
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            current_case = handle_generate_case()

        elif choice == "2":
            current_case = handle_load_case()

        elif choice == "3":
            if current_case:
                display_timeline(current_case)
            else:
                print("No case loaded yet. Use option 1 or 2 first.")

        elif choice == "4":
            if current_case:
                display_conflicts(current_case)
            else:
                print("No case loaded yet. Use option 1 or 2 first.")

        elif choice == "5":
            if current_case:
                handle_generate_report(current_case)
            else:
                print("No case loaded yet. Use option 1 or 2 first.")

        elif choice == "6":
            print("Exiting Alibi Engine. Goodbye!")
            break

        else:
            print("Invalid option, please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
