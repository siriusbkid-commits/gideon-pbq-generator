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
    toggle_student_mode,
    STUDENT_MODE
)

SCENARIO_DIR = "scenarios"


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
    # If user typed a full path and it exists, use it
    if os.path.isfile(scenario_file):
        return scenario_file

    # Otherwise assume it's inside scenarios/
    candidate = os.path.join(SCENARIO_DIR, scenario_file)
    if os.path.isfile(candidate):
        return candidate

    # If still not found, return original (will error later)
    return scenario_file


def run_scenario(scenario_file):
    """Run run_chained.py with the selected scenario."""
    scenario_path = resolve_scenario_path(scenario_file)

    print(f"\nRunning scenario: {scenario_path}\n")
    subprocess.run([sys.executable, "run_chained.py", scenario_path])


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
        from utils.save_pbq import save_pbq_json, save_pbq_markdown

        json_path = save_pbq_json(pbq)
        md_path = save_pbq_markdown(pbq, student_mode=STUDENT_MODE)

        print("\nPBQ saved successfully:")
        print(f"- JSON: {json_path}")
        print(f"- Markdown: {md_path}")
        print("\n")


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


def main():
    scenarios = list_scenarios()

    if not scenarios:
        print("No scenarios found in /scenarios folder.")
        return

    while True:
        print_menu(scenarios)

        max_choice = len(scenarios) + 4
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
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

