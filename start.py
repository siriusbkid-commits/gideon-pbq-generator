import os
import subprocess
import sys
import json

from pbq.menu import (
    print_menu, get_menu_choice, get_yes_no, get_scenario_number,
    get_positive_int, get_category_choice, get_difficulty_choice,
    get_cysa_domain_choice, get_log_type_choice,
    toggle_student_mode, STUDENT_MODE
)

SCENARIO_DIR = "scenarios"

def list_scenarios():
    if not os.path.isdir(SCENARIO_DIR):
        return []
    return sorted([f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")])

def exit_sim():
    print("Thanks for using GIDEON. Stay safe out there in identity land.")
    sys.exit(0)

def resolve_scenario_path(scenario_file):
    if os.path.isfile(scenario_file):
        return scenario_file
    candidate = os.path.join(SCENARIO_DIR, scenario_file)
    if os.path.isfile(candidate):
        return candidate
    return scenario_file

def run_scenario(scenario_file):
    scenario_path = resolve_scenario_path(scenario_file)
    print("Running scenario: " + scenario_path)
    subprocess.run([sys.executable, "run_chained.py", scenario_path])

def run_pbq_only():
    print("=== PBQ-ONLY MODE ===")
    selected_category = get_category_choice()
    selected_difficulty = get_difficulty_choice()
    scenarios = list_scenarios()
    for i, s in enumerate(scenarios, start=1):
        print(str(i) + ". " + s)
    scenario_index = get_scenario_number(len(scenarios))
    scenario_file = scenarios[scenario_index - 1]
    scenario_path = resolve_scenario_path(scenario_file)
    try:
        with open(scenario_path, "r") as f:
            scenario = json.load(f)
    except Exception as e:
        print("Error loading scenario: " + str(e))
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
        print("PBQ generation failed.")
        return
    print(pbq)
    if get_yes_no("Save PBQ to file? (y/n): "):
        json_path = save_pbq_json(pbq)
        md_path = save_pbq_markdown(pbq, student_mode=STUDENT_MODE)
        print("Saved: " + json_path + ", " + md_path)

def run_pbq_batch():
    print("=== BATCH PBQ GENERATION ===")
    count = get_positive_int("How many PBQs to generate? ")
    scenarios = list_scenarios()
    for i, s in enumerate(scenarios, start=1):
        print(str(i) + ". " + s)
    scenario_index = get_scenario_number(len(scenarios))
    scenario_file = scenarios[scenario_index - 1]
    scenario_path = resolve_scenario_path(scenario_file)
    try:
        with open(scenario_path, "r") as f:
            scenario = json.load(f)
    except Exception as e:
        print("Error: " + str(e))
        return
    selected_category = get_category_choice()
    selected_difficulty = get_difficulty_choice()
    from pbq.generator import PBQGenerator, PBQContext
    from llm_factory import get_llm
    from utils.save_pbq import save_pbq_json, save_pbq_markdown, get_batch_output_dir
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
    for i in range(1, count + 1):
        pbq_id = "batch-" + str(i).zfill(3)
        pbq = generator.generate_pbq(ctx, pbq_id=pbq_id)
        if pbq is None:
            continue
        save_pbq_json(pbq, base_dir=batch_dir)
        save_pbq_markdown(pbq, base_dir=batch_dir, student_mode=STUDENT_MODE)
    print("Batch complete. Files saved in: " + batch_dir)

def run_cysa_pbq():
    print("=== CySA+ CS0-004 PBQ MODE ===")
    from pbq.cysa_plus_module import generate_cysa_pbq, get_weighted_cysa_pbq, display_pbq
    print("1. Single  2. Batch")
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    domain_filter = get_cysa_domain_choice()
    selected_difficulty = get_difficulty_choice()
    if selected_difficulty == "beginner":
        selected_difficulty = "intermediate"
    if mode == "1":
        pbq = get_weighted_cysa_pbq() if domain_filter is None else generate_cysa_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_pbq(pbq)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_cysa_pbq(pbq)
    else:
        count = get_positive_int("How many CySA+ PBQs? ")
        for i in range(1, count + 1):
            pbq = get_weighted_cysa_pbq() if domain_filter is None else generate_cysa_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_pbq(pbq)
                _save_cysa_pbq(pbq, silent=True)

def _save_cysa_pbq(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "cysa").replace("-", "_").lower()
    fn = os.path.join("output", "cysa_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - CySA+ CS0-004 Practice PBQ" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["exam", "id", "domain", "sub_topic", "objective", "difficulty", "exam_objectives"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
    if not silent:
        print("Saved: " + fn)
    return fn

def run_cysa_log_pbq():
    print("=== CySA+ CS0-004 LOG ANALYSIS MODE ===")
    from pbq.cysa_log_module import generate_log_pbq, display_log_pbq
    print("1. Single  2. Batch")
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    log_type_filter = get_log_type_choice()
    selected_difficulty = get_difficulty_choice()
    if selected_difficulty == "beginner":
        selected_difficulty = "intermediate"
    if mode == "1":
        pbq = generate_log_pbq(log_type_filter=log_type_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_log_pbq(pbq)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_log_pbq(pbq)
    else:
        count = get_positive_int("How many Log PBQs? ")
        for i in range(1, count + 1):
            pbq = generate_log_pbq(log_type_filter=log_type_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_log_pbq(pbq)
                _save_log_pbq(pbq, silent=True)

def _save_log_pbq(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "log").replace("-", "_").lower()
    fn = os.path.join("output", "cysa_log_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - CySA+ CS0-004 Log Analysis PBQ" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["exam", "id", "log_type", "attack_type", "objective", "difficulty", "exam_objectives"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
    if not silent:
        print("Saved: " + fn)
    return fn

def run_ot_ics_scenario():
    print("\n=== OT/ICS SECURITY SCENARIO MODE ===")
    print("Operational Technology and Industrial Control Systems Security\n")
    from pbq.ot_ics_module import generate_ot_scenario, display_ot_scenario
    from pbq.menu import get_ot_domain_choice
    print("1. Generate a single OT/ICS scenario")
    print("2. Generate a batch of OT/ICS scenarios\n")
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    domain_filter = get_ot_domain_choice()
    selected_difficulty = get_difficulty_choice()
    if mode == "1":
        pbq = generate_ot_scenario(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_ot_scenario(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this scenario to file? (y/n): "):
            _save_ot_scenario(pbq)
    else:
        count = get_positive_int("How many OT/ICS scenarios? ")
        for i in range(1, count + 1):
            pbq = generate_ot_scenario(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_ot_scenario(pbq, student_mode=STUDENT_MODE)
                _save_ot_scenario(pbq, silent=True)
        print("Batch complete!")

def _save_ot_scenario(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "ot").replace("-", "_").lower()
    fn = os.path.join("output", "ot_ics_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - OT/ICS Security Scenario" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["module", "id", "domain", "sub_topic", "objective", "difficulty", "frameworks", "real_world"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
        if not STUDENT_MODE and pbq.get("answers"):
            f.write(chr(10) + chr(10) + "=" * 70 + chr(10))
            f.write("MODEL ANSWERS" + chr(10))
            f.write("=" * 70 + chr(10))
            f.write(pbq.get("answers", ""))
    if not silent:
        print("Saved: " + fn)
    return fn

def run_iot_scenario():
    print("\n=== IoT SECURITY SCENARIO MODE ===")
    print("Internet of Things Security for IT Professionals\n")
    from pbq.iot_module import generate_iot_scenario, display_iot_scenario
    from pbq.menu import get_iot_domain_choice
    print("1. Generate a single IoT scenario")
    print("2. Generate a batch of IoT scenarios\n")
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    domain_filter = get_iot_domain_choice()
    selected_difficulty = get_difficulty_choice()
    if mode == "1":
        pbq = generate_iot_scenario(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_iot_scenario(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this scenario to file? (y/n): "):
            _save_iot_scenario(pbq)
    else:
        count = get_positive_int("How many IoT scenarios? ")
        for i in range(1, count + 1):
            pbq = generate_iot_scenario(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_iot_scenario(pbq, student_mode=STUDENT_MODE)
                _save_iot_scenario(pbq, silent=True)
        print("Batch complete!")

def _save_iot_scenario(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "iot").replace("-", "_").lower()
    fn = os.path.join("output", "iot_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - IoT Security Scenario" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["module", "id", "domain", "sub_topic", "objective", "difficulty", "frameworks", "real_world"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
    if not silent:
        print("Saved: " + fn)
    return fn

def run_sc300_pbq():
    print("\n=== SC-300 PBQ MODE ===")
    print("Microsoft Identity and Access Administrator\n")
    from pbq.sc300_module import generate_sc300_pbq, get_weighted_sc300_pbq, display_sc300_pbq
    from pbq.sc300_search_patch import (
        generate_sc300_pbq_by_id,
        display_sc300_pbq_with_nudge,
        show_sc300_scenario_index,
    )
    from pbq.menu import get_sc300_domain_choice

    print("1. Single  2. Batch  S. Search by Scenario ID  ?. Show all Scenario IDs")

    # -- Mode selection ----------------------------------------
    while True:
        mode = input("Select mode (1, 2, S or ?): ").strip()
        if mode in ("1", "2", "S", "s", "?"):
            break
        print("Please enter 1, 2, S or ?.")

    # -- ? -- Show scenario index -------------------------------
    if mode == "?":
        show_sc300_scenario_index()
        return

    # -- S -- Search by Scenario ID -----------------------------
    if mode.upper() == "S":
        sid = input("  Enter Scenario ID (e.g. SC2-003): ").strip()
        pbq, err = generate_sc300_pbq_by_id(sid)
        if err:
            print(f"\n  [!]  {err}\n")
            return
        display_sc300_pbq_with_nudge(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_sc300_pbq(pbq)
        return

    # -- 1 / 2 -- Normal random / batch mode -------------------
    domain_filter = get_sc300_domain_choice()
    selected_difficulty = get_difficulty_choice()
    if selected_difficulty == "beginner":
        selected_difficulty = "intermediate"

    if mode == "1":
        pbq = get_weighted_sc300_pbq() if domain_filter is None else generate_sc300_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_sc300_pbq(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_sc300_pbq(pbq)
    else:
        count = get_positive_int("How many SC-300 PBQs? ")
        for i in range(1, count + 1):
            pbq = get_weighted_sc300_pbq() if domain_filter is None else generate_sc300_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_sc300_pbq(pbq, student_mode=STUDENT_MODE)
                _save_sc300_pbq(pbq, silent=True)
        print("Batch complete!")

def _save_sc300_pbq(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "sc300").replace("-", "_").lower()
    fn = os.path.join("output", "sc300_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - SC-300 Microsoft Identity and Access Administrator PBQ" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["exam", "id", "domain", "sub_topic", "objective", "difficulty", "exam_objectives"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
    if not silent:
        print("Saved: " + fn)
    return fn


def run_cyberark_pbq():
    print("\n=== CyberArk Defender PAM-DEF PBQ MODE ===")
    print("Privileged Access Management\n")
    from pbq.cyberark_defender_module import generate_cyberark_pbq, get_weighted_cyberark_pbq, display_cyberark_pbq
    from pbq.menu import get_cyberark_domain_choice
    print("1. Single  2. Batch")
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    domain_filter = get_cyberark_domain_choice()
    selected_difficulty = get_difficulty_choice()
    if selected_difficulty == "beginner":
        selected_difficulty = "intermediate"
    if mode == "1":
        pbq = get_weighted_cyberark_pbq() if domain_filter is None else generate_cyberark_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
        if "error" in pbq:
            print(pbq["error"])
            return
        display_cyberark_pbq(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_cyberark_pbq(pbq)
    else:
        count = get_positive_int("How many CyberArk Defender PBQs? ")
        for i in range(1, count + 1):
            pbq = get_weighted_cyberark_pbq() if domain_filter is None else generate_cyberark_pbq(domain_filter=domain_filter, difficulty_filter=selected_difficulty)
            if "error" not in pbq:
                display_cyberark_pbq(pbq, student_mode=STUDENT_MODE)
                _save_cyberark_pbq(pbq, silent=True)
        print("Batch complete!")


def _save_cyberark_pbq(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "cyberark").replace("-", "_").lower()
    fn = os.path.join("output", "cyberark_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - CyberArk Defender PAM-DEF PBQ" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["exam", "id", "domain", "sub_topic", "objective", "difficulty", "exam_objectives"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write(pbq.get("scenario", ""))
    if not silent:
        print("Saved: " + fn)
    return fn

def run_case_study_mode():
    print("\n=== SC-300 CASE STUDY MODE ===")
    print("10 full case studies, 80 MCQs, 50-pattern exam library\n")
    from pbq.case_study_module import (
        generate_case_study_pbq,
        get_weighted_case_study_pbq,
        generate_case_study_pbq_by_id,
        get_case_study_full_formatted,
        show_case_study_scenario_index,
        search_pattern_library,
        display_case_study_pbq,
        display_case_study_briefing,
    )
    from pbq.menu import get_sc300_domain_choice, get_case_study_choice, get_pattern_search_query

    print("3. FULL CASE STUDY WALKTHROUGH -- most like the real exam")
    print("   (Environment + Requirements shown first, then all 8 questions in order)")
    print()
    print("1. Single Random Question    2. Batch of Random Questions")
    print("4. Final Boss Only (CS10 -- all domains integrated)")
    print("B. View Case Study Briefing only (Environment + BR/SR/TR, no questions)")
    print("P. Search Pattern Library    S. Search by Question ID    ?. Show all Question IDs")

    # -- Mode selection ----------------------------------------
    while True:
        mode = input("Select mode (1, 2, 3, 4, B, P, S or ?): ").strip()
        if mode in ("1", "2", "3", "4", "B", "b", "P", "p", "S", "s", "?"):
            break
        print("Please enter 1, 2, 3, 4, B, P, S or ?.")

    # -- ? -- Show question index -------------------------------
    if mode == "?":
        show_case_study_scenario_index()
        return

    # -- B -- View Case Study Briefing on demand -----------------
    if mode.upper() == "B":
        cs_id = get_case_study_choice()
        display_case_study_briefing(cs_id)
        return

    # -- S -- Search by Question ID -----------------------------
    if mode.upper() == "S":
        qid = input("  Enter Question ID (e.g. CS4-Q6): ").strip()
        pbq, err = generate_case_study_pbq_by_id(qid)
        if err:
            print(f"\n  [!]  {err}\n")
            return
        display_case_study_pbq(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_case_study_pbq(pbq)
        return

    # -- P -- Search Pattern Library ----------------------------
    if mode.upper() == "P":
        keyword = get_pattern_search_query()
        results = search_pattern_library(keyword)
        if not results:
            print(f"\n  No patterns found matching '{keyword}'.\n")
            return
        print(f"\n{len(results)} pattern(s) found:\n")
        for p in results:
            print(f"  [Domain {p['domain']}] {p['pattern']}")
            print(f"    Sources: {', '.join(p['sources'])}\n")
        return

    # -- 3 -- Work through one Case Study in order --------------
    if mode == "3":
        cs_id = get_case_study_choice()
        meta, questions = get_case_study_full_formatted(cs_id)
        if not questions:
            print(f"\n  [!]  No questions found for {cs_id}.\n")
            return
        display_case_study_briefing(cs_id)
        input("Press ENTER to begin Question 1...\n")
        for i, pbq in enumerate(questions, start=1):
            display_case_study_pbq(pbq, student_mode=STUDENT_MODE)
            if get_yes_no("Save this PBQ to file? (y/n): "):
                _save_case_study_pbq(pbq)
            if i < len(questions):
                input("Press ENTER for next question...\n")
        print(f"\n{cs_id} complete!")
        return

    # -- 4 -- Final Boss only (CS10) -----------------------------
    if mode == "4":
        count = get_positive_int("How many Final Boss (CS10) questions? ")
        for i in range(1, count + 1):
            pbq = generate_case_study_pbq(case_study_filter="CS10")
            display_case_study_pbq(pbq, student_mode=STUDENT_MODE)
            _save_case_study_pbq(pbq, silent=True)
        print("Final Boss round complete!")
        return

    # -- 1 / 2 -- Normal random / batch mode --------------------
    domain_filter = get_sc300_domain_choice()

    if mode == "1":
        pbq = get_weighted_case_study_pbq() if domain_filter is None else generate_case_study_pbq(domain_filter=domain_filter)
        display_case_study_pbq(pbq, student_mode=STUDENT_MODE)
        if get_yes_no("Save this PBQ to file? (y/n): "):
            _save_case_study_pbq(pbq)
    else:
        count = get_positive_int("How many Case Study PBQs? ")
        for i in range(1, count + 1):
            pbq = get_weighted_case_study_pbq() if domain_filter is None else generate_case_study_pbq(domain_filter=domain_filter)
            display_case_study_pbq(pbq, student_mode=STUDENT_MODE)
            _save_case_study_pbq(pbq, silent=True)
        print("Batch complete!")


def _save_case_study_pbq(pbq, silent=False):
    import datetime
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = pbq.get("id", "casestudy").replace("-", "_").lower()
    fn = os.path.join("output", "casestudy_" + slug + "_" + ts + ".txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("GIDEON - SC-300 Case Study PBQ" + chr(10))
        f.write("=" * 70 + chr(10))
        for k in ["exam", "id", "case_study", "domain", "difficulty"]:
            f.write(k + ": " + str(pbq.get(k, "")) + chr(10))
        f.write("=" * 70 + chr(10) + chr(10))
        f.write("Context: " + pbq.get("context", "") + chr(10) + chr(10))
        f.write(pbq.get("question", "") + chr(10))
        for letter, text in pbq.get("options", {}).items():
            f.write(f"  {letter}. {text}" + chr(10))
        f.write(chr(10) + "CORRECT ANSWER: " + str(pbq.get("correct", "?")) + chr(10))
        f.write(chr(10) + pbq.get("explanation", "") + chr(10))
        refs = pbq.get("pattern_refs", [])
        if refs:
            f.write(chr(10) + "Pattern(s): " + "; ".join(refs) + chr(10))
    if not silent:
        print("Saved: " + fn)
    return fn


def main():
    scenarios = list_scenarios()
    if not scenarios:
        print("No scenarios found in /scenarios folder.")
        return
    while True:
        print_menu(scenarios)
        max_choice = len(scenarios) + 11
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
        elif choice == len(scenarios) + 6:
            run_cysa_log_pbq()
        elif choice == len(scenarios) + 7:
            run_ot_ics_scenario()
        elif choice == len(scenarios) + 8:
            run_iot_scenario()
        elif choice == len(scenarios) + 9:
            run_sc300_pbq()
        elif choice == len(scenarios) + 10:
            run_cyberark_pbq()
        elif choice == len(scenarios) + 11:
            run_case_study_mode()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()