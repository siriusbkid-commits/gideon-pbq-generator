import os
import subprocess
import sys
import json

# Import menu + input functions from pbq/menu.py
from pbq.menu import (
    print_menu,
    get_menu_choice,
    get_yes_no,
    get_scenario_number,
    get_positive_int,
    get_category_choice,
    get_difficulty_choice,
    get_cysa_domain_choice,
    toggle_student_mode,
    STUDENT_MODE
)

SCENARIO_DIR = "scenarios"


# ============================================================
# Scenario Helpers
# ============================================================

def list_scenarios():
    """Return a list of all .json scenario files."""
    if not os.path.isdir(SCENARIO_DIR):
        return []
    files = [f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")]
    return sorted(files)


def exit_sim():
    """Clean exit message."""
    print("\nThanks for using GIDEON. Stay safe out there in identity land.\n")
    sys.exit(0)


def resolve_scenario_path(scenario_file):
    """
    Ensure the scenario path is valid.
    If the user only typed a filename, prepend the scenarios/ directory.
    """
    if os.path.isfile(scenario_file):
        return scenario_file

    candidate = os.path.join(SCENARIO_DIR, scenario_file)
    if os.path.isfile(candidate):
        return candidate

    return scenario_file


def run_scenario(scenario_file):
    """Run run_chained.py with the selected scenario."""
    scenario_path = resolve_scenario_path(scenario_file)

    print(f"\nRunning scenario: {scenario_path}\n")
    subprocess.run([sys.executable, "run_chained.py", scenario_path])


# ============================================================
# PBQ-ONLY MODE
# ============================================================

def run_pbq_only():
    """Generate a PBQ directly without running the IAM chain."""
    print("\n=== PBQ-ONLY MODE ===\n")

    selected_category = get_category_choice()
    selected_difficulty = get_difficulty_choice()

    scenarios = list_scenarios()
    print("\nAvailable scenarios:\n")
    for i, s in enumerate(scenarios, start=1):
        print(f"{i}. {s}")

    scenario_index = get_scenario_number(len(scenarios))
    scenario_file = scenarios[scenario_index - 1]
    scenario_path = resolve_scenario_path(scenario_file)

    try:
        with open(scenario_path, "r") as f:
            scenario = json.load(f)
    except Exception as e:
        print(f"Error loading scenario: {e}")
        return

    from pbq.generator import PBQGenerator, PBQContext
    from llm_factory import get_llm
    from utils.save_pbq import save_pbq_json, save_pbq_markdown

    llm = get_llm()
    generator = PBQGenerator(llm)

    ctx = PBQContext(
        scenario_id=scenario["id"],
        title=scenario["metadata"]["title"],
        summary=scenario["metadata"].get("summary", "No summary provided."),
        actors=scenario["metadata"].get("actors", []),
        systems=scenario["metadata"].get("systems", []),
        risks_findings=scenario["metadata"].get("risks", []),
        controls_in_scope=scenario["metadata"].get("controls", []),
        learning_objectives=scenario["metadata"]["learning_objectives"],
        difficulty=selected_difficulty,
        category=selected_category
    )

    pbq = generator.generate_pbq(ctx, pbq_id="pbq-only-001")

    if pbq is None:
        print("⚠ PBQ generation failed after retries. Skipping.\n")
        return

    print("\n=== PBQ GENERATED ===\n")
    print(pbq)
    print("\n======================\n")

    if get_yes_no("Save PBQ to file? (y/n): "):
        json_path = save_pbq_json(pbq)
        md_path = save_pbq_markdown(pbq, student_mode=STUDENT_MODE)

        print("\nPBQ saved successfully:")
        print(f"- JSON: {json_path}")
        print(f"- Markdown: {md_path}")
        print("\n")


# ============================================================
# BATCH PBQ MODE
# ============================================================

def run_pbq_batch():
    """Generate multiple PBQs and save them into a unique batch folder."""
    print("\n=== BATCH PBQ GENERATION ===\n")

    count = get_positive_int("How many PBQs to generate? (e.g., 5, 10, 20): ")

    scenarios = list_scenarios()
    print("\nAvailable scenarios:\n")
    for i, s in enumerate(scenarios, start=1):
        print(f"{i}. {s}")

    scenario_index = get_scenario_number(len(scenarios))
    scenario_file = scenarios[scenario_index - 1]
    scenario_path = resolve_scenario_path(scenario_file)

    try:
        with open(scenario_path, "r") as f:
            scenario = json.load(f)
    except Exception as e:
        print(f"Error loading scenario: {e}")
        return

    selected_category = get_category_choice()
    selected_difficulty = get_difficulty_choice()

    from pbq.generator import PBQGenerator, PBQContext
    from llm_factory import get_llm
    from utils.save_pbq import (
        save_pbq_json,
        save_pbq_markdown,
        get_batch_output_dir
    )

    llm = get_llm()
    generator = PBQGenerator(llm)

    ctx = PBQContext(
        scenario_id=scenario["id"],
        title=scenario["metadata"]["title"],
        summary=scenario["metadata"].get("summary", "No summary provided."),
        actors=scenario["metadata"].get("actors", []),
        systems=scenario["metadata"].get("systems", []),
        risks_findings=scenario["metadata"].get("risks", []),
        controls_in_scope=scenario["metadata"].get("controls", []),
        learning_objectives=scenario["metadata"]["learning_objectives"],
        difficulty=selected_difficulty,
        category=selected_category
    )

    batch_dir = get_batch_output_dir()
    print(f"\nBatch folder created: {batch_dir}\n")

    for i in range(1, count + 1):
        pbq_id = f"batch-{i:03d}"
        print(f"[{i}/{count}] Generating PBQ {pbq_id}...")

        pbq = generator.generate_pbq(ctx, pbq_id=pbq_id)

        if pbq is None:
            print(f"⚠ Skipping PBQ {pbq_id} due to repeated JSON errors.\n")
            continue

        json_path = save_pbq_json(pbq, base_dir=batch_dir)
        md_path = save_pbq_markdown(pbq, base_dir=batch_dir, student_mode=STUDENT_MODE)

        print(f"Saved JSON → {json_path}")
        print(f"Saved MD   → {md_path}\n")

    print("\n=== Batch PBQ Generation Complete ===")
    print(f"All files saved in: {batch_dir}\n")


# ============================================================
# CYSA+ CS0-004 PBQ MODE
# ============================================================

def run_cysa_pbq():
    """Generate CySA+ CS0-004 PBQs using the local template engine.
    No LLM required — instant generation from randomised scenario templates."""

    print("\n=== CySA+ CS0-004 PBQ MODE ===")
    print("CompTIA Cybersecurity Analyst — V4 (Launches June 23, 2026)\n")

    from pbq.cysa_plus_module import generate_cysa_pbq, get_weighted_cysa_pbq, display_pbq

    # Ask: single or batch
    print("1. Generate a single CySA+ PBQ")
    print("2. Generate a batch of CySA+ PBQs\n")

    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    # Domain selection
    domain_filter = get_cysa_domain_choice()

    # Difficulty selection
    selected_difficulty = get_difficulty_choice()
    # Note: our templates use intermediate/advanced — beginner maps to intermediate
    if selected_difficulty == "beginner":
        selected_difficulty = "intermediate"
        print("(Note: CySA+ is an intermediate-level exam — using Intermediate difficulty)\n")

    # ── Single mode ──
    if mode == "1":
        if domain_filter is None:
            pbq = get_weighted_cysa_pbq()
        else:
            pbq = generate_cysa_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)

        if "error" in pbq:
            print(f"\n⚠ {pbq['error']}\n")
            return

        display_pbq(pbq)

        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_cysa_pbq(pbq)

    # ── Batch mode ──
    else:
        count = get_positive_int("How many CySA+ PBQs to generate? (e.g., 5, 10, 20): ")

        saved = []
        for i in range(1, count + 1):
            print(f"[{i}/{count}] Generating CySA+ PBQ...")

            if domain_filter is None:
                pbq = get_weighted_cysa_pbq()
            else:
                pbq = generate_cysa_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)

            if "error" in pbq:
                print(f"  ⚠ {pbq['error']} — skipping.\n")
                continue

            display_pbq(pbq)
            path = _save_cysa_pbq(pbq, silent=True)
            saved.append(path)
            print(f"  Saved → {path}\n")

        print(f"\n=== CySA+ Batch Complete — {len(saved)} PBQs saved ===\n")


def _save_cysa_pbq(pbq: dict, silent: bool = False) -> str:
    """Save a CySA+ PBQ to the output folder as a .txt file."""
    import datetime

    os.makedirs("output", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_slug = pbq.get("id", "cysa").replace("-", "_").lower()
    filename = f"output/cysa_{domain_slug}_{timestamp}.txt"

    lines = [
        f"GIDEON — CySA+ CS0-004 Practice PBQ",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 70,
        f"Exam       : {pbq.get('exam', '')}",
        f"ID         : {pbq.get('id', '')}",
        f"Domain     : {pbq.get('domain', '')}",
        f"Sub-topic  : {pbq.get('sub_topic', '')}",
        f"Objective  : {pbq.get('objective', '')}",
        f"Difficulty : {pbq.get('difficulty', '').upper()}",
        f"Obj. Refs  : {pbq.get('exam_objectives', '')}",
        "=" * 70,
        "",
        pbq.get("scenario", ""),
        "",
        "=" * 70,
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    if not silent:
        print(f"\nPBQ saved → {filename}\n")

    return filename


# ============================================================
# MAIN MENU LOOP
# ============================================================

def main():
    scenarios = list_scenarios()

    if not scenarios:
        print("No scenarios found in /scenarios folder.")
        return

    while True:
        print_menu(scenarios)

        # Now 5 fixed options after the scenario list
        max_choice = len(scenarios) + 5
        choice = get_menu_choice(max_choice)

        if 1 <= choice <= len(scenarios):
            run_scenario(scenarios[choice - 1])
        elif choice == len(scenarios) + 1:
            exit_sim()
        elif choice == len(scenarios) + 2:
            run_pbq_only()
        elif choice == len(scenarios) + 3:
            run_pbq_batch()
        elif choice == len(scenarios) + 4:
            toggle_student_mode()
        elif choice == len(scenarios) + 5:
            run_cysa_pbq()
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()