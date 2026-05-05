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
# Save PBQ as Markdown (Instructor + Student)
# ============================================================

def save_pbq_markdown(pbq, base_dir="pbq_output", student_mode=False):
    """
    Saves either:
      - Instructor Markdown (full rationales)
      - Student Markdown (no rationales, no answers)
    """
    folder = ensure_output_folder(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if student_mode:
        filename = f"pbq_{pbq.id}_{timestamp}_student.md"
        md_content = pbq.to_markdown_student()
    else:
        filename = f"pbq_{pbq.id}_{timestamp}_instructor.md"
        md_content = pbq.to_markdown_instructor()

    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return path


# ============================================================
# Batch PBQ Output Directory Helper
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

