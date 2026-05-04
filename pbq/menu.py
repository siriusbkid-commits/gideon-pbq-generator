# pbq/menu.py

STUDENT_MODE = False

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
# Input Guardrails
# =========================

def get_menu_choice(max_choice: int) -> int:
    while True:
        choice = input("Enter your choice: ").strip()
        if choice.isdigit():
            choice_int = int(choice)
            if 1 <= choice_int <= max_choice:
                return choice_int
        print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")


def get_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def get_scenario_number(max_num: int) -> int:
    while True:
        val = input(f"Select a scenario number (1–{max_num}): ").strip()
        if val.isdigit():
            num = int(val)
            if 1 <= num <= max_num:
                return num
        print(f"Invalid selection. Please enter a number between 1 and {max_num}.")


def get_positive_int(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Invalid number. Please enter a positive integer.")


def get_category_choice() -> str:
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
    print(f"\nGideon is now in: {mode}\n"
