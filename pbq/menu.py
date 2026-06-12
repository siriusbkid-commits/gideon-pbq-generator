# pbq/menu.py

STUDENT_MODE = False


def print_menu(scenarios):
    print("\n========================================")
    print(" GIDEON: Identity Attack Simulator")
    print("========================================\n")
    print("Choose an option:\n")
    for i, scenario in enumerate(scenarios, start=1):
        print(f"{i}. Run scenario -> {scenario}")
    print(f"{len(scenarios) + 1}. Exit")
    print(f"{len(scenarios) + 2}. PBQ-Only Mode (Generate PBQ without IAM chain)")
    print(f"{len(scenarios) + 3}. Batch PBQ Mode (Generate multiple PBQs)")
    print(f"{len(scenarios) + 4}. Toggle Student Mode (Hide/Show Rationales)")
    print(f"{len(scenarios) + 5}. CySA+ CS0-004 PBQ Mode (Generate CySA+ Practice Questions)")
    print(f"{len(scenarios) + 6}. CySA+ CS0-004 Log Analysis Mode (Generate Log Analysis PBQs)")
    print(f"{len(scenarios) + 7}. OT/ICS Security Scenarios (Generate OT/ICS Practice Scenarios)\n")
    mode = "STUDENT MODE (Rationales Hidden)" if STUDENT_MODE else "INSTRUCTOR MODE (Rationales Visible)"
    print(f"Current Mode: {mode}\n")


def get_menu_choice(max_choice):
    while True:
        choice = input("Enter your choice: ").strip()
        if choice.isdigit():
            choice_int = int(choice)
            if 1 <= choice_int <= max_choice:
                return choice_int
        print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")


def get_yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"): return True
        if ans in ("n", "no"): return False
        print("Please enter y or n.")


def get_scenario_number(max_num):
    while True:
        val = input(f"Select a scenario number (1-{max_num}): ").strip()
        if val.isdigit():
            num = int(val)
            if 1 <= num <= max_num:
                return num
        print(f"Invalid selection. Please enter a number between 1 and {max_num}.")


def get_positive_int(prompt):
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Invalid number. Please enter a positive integer.")


def get_category_choice():
    print("\nChoose PBQ Category:\n")
    print("1. SC-300 (Microsoft Identity)")
    print("2. IAM Fundamentals")
    print("3. Governance & Compliance")
    print("4. CyberArk Defender")
    print("5. Vendor-Neutral IAM")
    print("6. CySA+ CS0-004\n")
    categories = {
        "1": "SC-300", "2": "IAM Fundamentals",
        "3": "Governance & Compliance", "4": "CyberArk Defender",
        "5": "Vendor-Neutral IAM", "6": "CySA+ CS0-004",
    }
    while True:
        cat_choice = input("Select a category number: ").strip()
        if cat_choice in categories:
            return categories[cat_choice]
        print("Invalid category. Please enter a number between 1 and 6.")


def get_difficulty_choice():
    print("\nChoose Difficulty:\n")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Advanced\n")
    difficulties = {"1": "beginner", "2": "intermediate", "3": "advanced"}
    while True:
        diff_choice = input("Select a difficulty number: ").strip()
        if diff_choice in difficulties:
            return difficulties[diff_choice]
        print("Invalid difficulty. Please enter 1, 2, or 3.")


def get_cysa_domain_choice():
    print("\nChoose CySA+ CS0-004 Domain:\n")
    print("1. Security Operations          (34%)")
    print("2. Vulnerability Management     (26%)")
    print("3. Incident Response & Mgmt     (24%)")
    print("4. Reporting & Communication    (16%)")
    print("5. Random (weighted by exam %)\n")
    domains = {"1": "1", "2": "2", "3": "3", "4": "4", "5": None}
    while True:
        choice = input("Select a domain number: ").strip()
        if choice in domains:
            return domains[choice]
        print("Invalid choice. Please enter a number between 1 and 5.")


def get_log_type_choice():
    print("\nChoose Log Type:\n")
    print("1. Windows Security Event Logs")
    print("2. Firewall / Network Logs")
    print("3. DNS Logs")
    print("4. Authentication / IAM Logs")
    print("5. IDS/IPS Logs")
    print("6. Web Server / Application Logs")
    print("7. Random (any log type)\n")
    log_types = {
        "1": "windows", "2": "firewall", "3": "dns",
        "4": "auth", "5": "ids", "6": "web", "7": None,
    }
    while True:
        choice = input("Select a log type number: ").strip()
        if choice in log_types:
            return log_types[choice]
        print("Invalid choice. Please enter a number between 1 and 7.")


def toggle_student_mode():
    global STUDENT_MODE
    STUDENT_MODE = not STUDENT_MODE
    mode = "STUDENT MODE (Rationales Hidden)" if STUDENT_MODE else "INSTRUCTOR MODE (Rationales Visible)"
    print(f"\nGideon is now in: {mode}\n")

def get_ot_domain_choice() -> str:
    print("\nChoose OT/ICS Domain:\n")
    print("1. Architecture (Purdue Model, Protocols)")
    print("2. Threat Landscape (Nation-state, Ransomware)")
    print("3. Defensive Controls (IEC 62443, Vulnerability Mgmt)")
    print("4. Incident Response")
    print("5. Random (any domain)\n")
    domains = {
        "1": "architecture",
        "2": "threats",
        "3": "defensive",
        "4": "incident_response",
        "5": None,
    }
    while True:
        choice = input("Select a domain number: ").strip()
        if choice in domains:
            return domains[choice]
        print("Invalid choice. Please enter a number between 1 and 5.")

def get_ot_domain_choice() -> str:
    print("\nChoose OT/ICS Domain:\n")
    print("1. Architecture (Purdue Model, Protocols)")
    print("2. Threat Landscape (Nation-state, Ransomware)")
    print("3. Defensive Controls (IEC 62443, Vulnerability Mgmt)")
    print("4. Incident Response")
    print("5. Random (any domain)\n")
    domains = {
        "1": "architecture",
        "2": "threats",
        "3": "defensive",
        "4": "incident_response",
        "5": None,
    }
    while True:
        choice = input("Select a domain number: ").strip()
        if choice in domains:
            return domains[choice]
        print("Invalid choice. Please enter a number between 1 and 5.")
