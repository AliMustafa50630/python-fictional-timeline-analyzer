# Fictional Timeline Analyzer
A Python command-line project that analyzes fictional event timelines, detects scheduling and travel conflicts, and generates a simple consistency report.

>  **This is a fictional simulation project built for practicing Python.**
> All characters, locations, and events are synthetic. This project is not
> intended for, and must not be used for, real-world deception or creating
> real alibis. It exists purely to demonstrate core Python programming
> concepts through a fun, self-contained logic puzzle.

## Purpose

This project was built as a beginner-to-intermediate Python portfolio piece.
Instead of another to-do list or calculator, it wraps common Python
fundamentals in a small "detective logic" theme: build a timeline, then use
plain rule-based checks to see if it holds together.

## Features

- Generate fictional characters, locations, and events with random but
  realistic timestamps
- Load and analyze an existing case from a JSON file
- Build a sorted, per-character chronological timeline
- Detect **overlapping events** (a character "double-booked" in time)
- Detect **impossible presence** (a character in two different places at once)
- Detect **insufficient travel time** between two different locations
- Calculate a transparent, rule-based **consistency score** (0–100)
- Generate a clear, readable final report and save it to a text file
- Simple, guided command-line menu — no setup or arguments required

## Python Concepts Demonstrated

- Variables and core data types (strings, ints, floats, booleans)
- `if` / `elif` / `else` branching
- `for` and `while` loops, including nested loops
- Functions with parameters, return values, and default arguments
- Lists and list comprehensions
- Dictionaries (including nested dictionaries)
- Sets (used to guarantee unique character names)
- String formatting with f-strings
- The `datetime` module for parsing, comparing, and formatting timestamps
- The `random` module for generating fictional scenarios
- File handling (reading/writing JSON and plain text files)
- Basic exception handling (`try` / `except`) for file and input errors

No web frameworks, databases, APIs, or machine learning are used.

## Project Structure

```
alibi-engine/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py         # CLI menu and program flow
│   ├── generator.py    # Creates fictional characters, locations, events
│   ├── timeline.py     # Builds timelines and detects conflicts
│   └── report.py       # Scores consistency and builds the final report
└── data/
    └── sample_case.json  # A ready-to-use fictional case for demo purposes
```

## How the Timeline Engine Works

1. **Generation** (`generator.py`) creates a set of characters and, for each
   one, a sequence of events with a location, activity, and start/end time.
   Gaps between events are randomized (and can occasionally be very short or
   negative), which naturally produces some conflicts to detect later.

2. **Timeline building** (`timeline.py`) sorts each character's events by
   start time, then compares events to each other using simple time-range
   logic:
   - Two events **overlap** if one starts before the other ends and vice
     versa.
   - If two overlapping events happen at **different locations**, that is
     flagged as an **Impossible Presence** — the character cannot logically
     be in two places at once.
   - If two overlapping events happen at the **same location**, that is
     flagged as a **Duplicate Booking**.
   - If two consecutive, non-overlapping events are at different locations
     but leave less than a configurable travel buffer (default 15 minutes)
     between them, that is flagged as **Insufficient Travel Time**.

3. **Scoring** (`report.py`) starts every case at a perfect score of 100 and
   subtracts fixed, transparent penalty points for each conflict type:

   | Conflict Type              | Penalty |
   |-----------------------------|---------|
   | Impossible Presence         | -25     |
   | Duplicate Booking           | -10     |
   | Insufficient Travel Time    | -8      |

   The final score (never below 0) is translated into a plain-English
   verdict: *Highly Consistent*, *Mostly Consistent*, *Questionable*, or
   *Highly Inconsistent*. There is no AI or machine learning involved — it is
   a fixed, readable set of rules anyone can follow by hand.

## Example Output

```
============================================================
ALIBI ENGINE REPORT - Lahore Timeline Case
============================================================
Generated on: 2026-08-20 07:00
Characters involved: Ali Khan, Ayesha Malik, Hira Qureshi
Total events recorded: 10

------------------------------------------------------------
CONFLICTS DETECTED
------------------------------------------------------------
  [Impossible Presence] Ayesha Malik
    - 2026-08-20 08:00 to 2026-08-20 09:00 at Quaid-e-Azam Library(Studying at the library)
    - 2026-08-20 08:30 to 2026-08-20 09:30 at Gulberg Cafe (Meeting a friend)

  [Insufficient Travel Time] Hira Qureshi
    - 2026-08-20 09:00 to 2026-08-20 10:30 at Liberty Market (Shopping)
    - 2026-08-20 10:32 to 2026-08-20 11:30 at Fortress Square (Having dinner)
    - Only 2.0 minutes available to travel

  [Insufficient Travel Time] Hira Qureshi
    - 2026-08-20 10:32 to 2026-08-20 11:30 at Fortress Square (Having dinner)
    - 2026-08-20 11:35 to 2026-08-20 12:15 at Model Town Park (Taking a walk)
    - Only 5.0 minutes available to travel

------------------------------------------------------------
CONSISTENCY SCORE
------------------------------------------------------------
  Score: 59/100
  Verdict: Questionable
============================================================
```

## Installation

Requires Python 3.8 or later. No external packages are needed.

```bash
git clone https://github.com/AliMustafa50630/python-fictional-timeline-analyzer.git
cd python-fictional-timeline-analyzer
```

## How to Run

```bash
cd src
python main.py
```

Then follow the on-screen menu:

```
1. Generate fictional case
2. Analyze existing case
3. Display timeline
4. Check conflicts
5. Generate report
6. Exit
```

Choosing **option 2** and pressing Enter without typing a path will load the
bundled `data/sample_case.json`, so the program can be explored immediately
without any setup.

## Limitations

- Travel time between locations is checked against one fixed buffer
  (15 minutes) rather than real distances or travel modes.
- All data is single-day and single-timezone for simplicity.
- The consistency score uses fixed penalty weights rather than
  context-aware or probabilistic reasoning.
- The CLI is single-session; nothing is persisted except the case and report
  files explicitly saved to `data/`.

## Future Improvements

- Support multi-day cases and timezones
- Estimate travel time based on real or configurable distances between
  named locations
- Add a location map or simple visualization of each character's movements
- Allow exporting reports as formatted PDF or HTML
- Add unit tests for the conflict-detection logic
