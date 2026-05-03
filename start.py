import os
import subprocess
import sys
import json

SCENARIO_DIR = "scenarios"

# =========================
# Student Mode Flag
# =========================
STUDENT_MODE = False


def list_scenarios():
    """Return a list of all .json scenario files."""
    files = [f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")]
    return sorted(files)


def print_menu(scenarios):
    print("\n========================================")
    print(" GIDEON: Identity Attack Simulator")
    print("========================================\n")
    print("Choose an option:\n")

    for i, scenario in enumerate(scenarios, start=1):
        print(f"{i}. Run scenario → {scenario}")

    print(f"{len(scenarios) + 1}. Exit")
    print(f"{len(scenarios) + 2}. PBQ-Only Mode (Generate PBQ without IAM chain)")
    print(f"{len(scenarios) + 3}. Batch PBQ Mode (Generate multiple PBQs)")
    print(f"{len(scenarios) + 4}. Toggle Student Mode (Hide/Show Rationales)\n")

    mode = "STUDENT MODE (Rationales Hidden)" if STUDENT_MODE else "INSTRUCTOR MODE (Rationales Visible)"
    print(f"Current Mode: {mode}\n")


# =========================
# Guardrail helper functions
# =========================

def get_menu_choice(max_choice: int) -> int:
    """Safely get a menu choice between 1 and max_choice."""
    while True:
        choice = input("Enter your choice: ").strip()
        if choice.isdigit():
            choice_int = int(choice)
            if 1 <= choice_int <= max_choice:
                return choice_int
        print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")


def get_yes_no(prompt: str) -> bool:
    """Safely get a yes/no answer."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_scenario_number(max_num: int) -> int:
    """Safely get a scenario number between 1 and max_num."""
    while True:
        val = input(f"Select a scenario number (1–{max_num}): ").strip()
        if val.isdigit():
            num = int(val)
            if 1 <= num <= max_num:
                return num
        print(f"Invalid selection. Please enter a number between 1 and {max_num}.")


def get_positive_int(prompt: str) -> int:
    """Safely get a positive integer."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Invalid number. Please enter a positive integer.")


def get_category_choice() -> str:
    """Safely get a PBQ category key."""
    print("\nChoose PBQ Category:\n")
    print("1. SC-300 (Microsoft Identity)")
    print("2. IAM Fundamentals")
    print("3. Governance & Compliance")
    print("4. CyberArk Defender")
    print("5. Vendor-Neutral IAM\n")

    categories = {
        "1": "SC-300",
        "2": "IAM Fundamentals",
        "3": "Governance & Compliance",
        "4": "CyberArk Defender",
        "5": "Vendor-Neutral IAM"
    }

    while True:
        cat_choice = input("Select a category number: ").strip()
        if cat_choice in categories:
            return categories[cat_choice]
        print("Invalid category. Please enter a number between 1 and 5.")


def get_difficulty_choice() -> str:
    """Safely get a difficulty level."""
    print("\nChoose Difficulty:\n")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Advanced\n")

    difficulties = {
        "1": "beginner",
        "2": "intermediate",
        "3": "advanced"
    }

    while True:
        diff_choice = input("Select a difficulty number: ").strip()
        if diff_choice in difficulties:
            return difficulties[diff_choice]
        print("Invalid difficulty. Please enter 1, 2, or 3.")


# =========================
# Student Mode Toggle
# =========================

def toggle_student_mode():
    global STUDENT_MODE
    STUDENT_MODE = not STUDENT_MODE
    mode = "STUDENT MODE (Rationales Hidden)" if STUDENT_MODE else "INSTRUCTOR MODE (Rationales Visible)"
    print(f"\nGideon is now in: {mode}\n")


def exit_sim():
    """Clean exit message."""
    print("\nThanks for using GIDEON. Stay safe out there in identity land.\n")
    sys.exit(0)


def run_scenario(scenario_file):
    """Run run_chained.py with the selected scenario."""
    print(f"\nRunning scenario: {scenario_file}\n")
    subprocess.run([sys.executable, "run_chained.py", scenario_file])


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
    scenario_path = f"{SCENARIO_DIR}/{scenario_file}"

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
    scenario_path = f"{SCENARIO_DIR}/{scenario_file}"

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
