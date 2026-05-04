import os
import json
from datetime import datetime


# ============================================================
# Ensure output folder exists
# ============================================================

def ensure_output_folder(base_dir="pbq_output"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir


# ============================================================
# Save PBQ as JSON
# ============================================================

def save_pbq_json(pbq, base_dir="pbq_output"):
    folder = ensure_output_folder(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pbq_{pbq.id}_{timestamp}.json"
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(pbq.to_json(), f, indent=2)

    return path


# ============================================================
# Save PBQ as Markdown (Student Mode supported)
# ============================================================

def save_pbq_markdown(pbq, base_dir="pbq_output", student_mode=False):
    folder = ensure_output_folder(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pbq_{pbq.id}_{timestamp}.md"
    path = os.path.join(folder, filename)

    md = []
    md.append(f"# {pbq.title}\n")
    md.append(f"**Difficulty:** {pbq.difficulty}")
    md.append(f"**Scenario ID:** {pbq.scenario_id}\n")
    md.append("## Scenario")
    md.append(pbq.stem + "\n")

    # Exhibits
    if pbq.exhibits:
        md.append("## Exhibits")
        for ex in pbq.exhibits:
            md.append(f"### {ex.label}")
            md.append(ex.content + "\n")

    # Tasks
    if pbq.tasks:
        md.append("## Tasks")
        for task in pbq.tasks:
            md.append(f"### Task {task.id}")
            md.append(task.prompt)

            md.append("\n**Options:**")
            for opt in task.options:
                md.append(f"- **{opt.id}** — {opt.text}")

            md.append("\n**Correct Options:**")
            md.append(", ".join(task.correct_options))

            # Rationale handling
            if student_mode:
                md.append("\n> **Rationales are hidden in Student Mode.**\n")
            else:
                md.append("\n**Rationale:**")
                for key, value in task.rationale.items():
                    md.append(f"- **{key}** — {value}")

            md.append("")  # spacing

    # Write file
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    return path


# ============================================================
# Batch PBQ Output Directory Helper (required by Start.py)
# ============================================================

def get_batch_output_dir():
    """
    Create and return a timestamped batch output directory.
    Used by Batch PBQ Mode in Start.py.
    """
    base_dir = os.path.join(os.getcwd(), "output", "batch_pbq")
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_dir = os.path.join(base_dir, f"batch_{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)

    return batch_dir

