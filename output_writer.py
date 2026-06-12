import json
import os
from datetime import datetime

def save_output(final_result: str, scenario_name: str = "default"):
    """
    Saves the final IAM simulator output in both JSON and TXT formats.
    """

    # Create output directory if missing
    os.makedirs("output", exist_ok=True)

    # Timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # File paths
    txt_path = f"output/{scenario_name}_{timestamp}.txt"
    json_path = f"output/{scenario_name}_{timestamp}.json"

    # Save TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(final_result)

    # Save JSON (wrapped in a dict)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"scenario": scenario_name, "result": final_result}, f, indent=4)

    return txt_path, json_path
