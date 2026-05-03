import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# ============================================================
# PBQ DATA STRUCTURES
# ============================================================

@dataclass
class PBQTaskOption:
    id: str
    text: str


@dataclass
class PBQTask:
    id: str
    type: str
    prompt: str
    options: List[PBQTaskOption]
    correct_options: List[str]
    rationale: Dict[str, str]


@dataclass
class PBQExhibit:
    id: str
    type: str
    label: str
    content: str


@dataclass
class PBQ:
    id: str
    scenario_id: str
    difficulty: str
    title: str
    stem: str
    exhibits: List[PBQExhibit]
    tasks: List[PBQTask]

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "difficulty": self.difficulty,
            "title": self.title,
            "stem": self.stem,
            "exhibits": [ex.__dict__ for ex in self.exhibits],
            "tasks": [
                {
                    "id": t.id,
                    "type": t.type,
                    "prompt": t.prompt,
                    "options": [opt.__dict__ for opt in t.options],
                    "correct_options": t.correct_options,
                    "rationale": t.rationale,
                }
                for t in self.tasks
            ],
        }


# ============================================================
# PBQ CONTEXT
# ============================================================

@dataclass
class PBQContext:
    scenario_id: str
    title: str
    summary: str
    actors: List[str]
    systems: List[str]
    risks_findings: List[str]
    controls_in_scope: List[str]
    learning_objectives: List[str]
    difficulty: str
    category: str


# ============================================================
# JSON EXTRACTION (HARDENED)
# ============================================================

def extract_last_json_block(text: str) -> str:
    """
    Extracts the FIRST valid JSON object in the text.
    Removes markdown, commentary, and stray characters.
    """
    cleaned = (
        text.replace("```json", "")
            .replace("```", "")
            .replace("\r", "")
            .strip()
    )

    starts = [i for i, ch in enumerate(cleaned) if ch == "{"]

    if not starts:
        raise ValueError("No JSON object found in LLM output.")

    for start in starts:
        brace_count = 0
        in_string = False

        for i in range(start, len(cleaned)):
            ch = cleaned[i]

            if ch == '"' and cleaned[i - 1] != "\\":
                in_string = not in_string

            if not in_string:
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1

                if brace_count == 0:
                    candidate = cleaned[start:i + 1].strip()
                    try:
                        json.loads(candidate)
                        return candidate
                    except Exception:
                        pass

    raise ValueError("No valid JSON object found in LLM output.")


# ============================================================
# PBQ GENERATOR (FULLY HARDENED)
# ============================================================

class PBQGenerator:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, ctx: PBQContext) -> str:
        """
        This is the strictest JSON-only PBQ prompt possible.
        It forbids multiline strings, markdown, commentary, and schema drift.
        """
        return f"""
You are an AI that outputs ONLY valid JSON. You MUST obey these rules with ZERO exceptions:

1. Output ONLY a single JSON object.
2. NO markdown, NO backticks, NO commentary, NO explanations.
3. ALL strings MUST be valid JSON strings.
4. You MUST escape ALL newline characters inside strings as \\n.
5. You MUST NOT output raw line breaks inside any JSON string.
6. You MUST NOT output placeholder values like <string>.
7. You MUST NOT output trailing commas.
8. You MUST NOT output keys that are not in the schema.
9. If you cannot produce valid JSON, output exactly: {{}}

Your JSON MUST match this schema EXACTLY:

{{
  "title": "PBQ: {ctx.title}",
  "stem": "<string>",
  "exhibits": [],
  "tasks": []
}}

Where:
- "stem" MUST be a concise, single-paragraph scenario description.
- "stem" MUST NOT contain unescaped newlines.
- "exhibits" MUST be an array (may be empty).
- "tasks" MUST be an array (may be empty).

SCENARIO CONTEXT (summarize into the PBQ stem):
Title: {ctx.title}
Summary: {ctx.summary}
Actors: {", ".join(ctx.actors)}
Systems: {", ".join(ctx.systems)}
Risks: {", ".join(ctx.risks_findings)}
Controls: {", ".join(ctx.controls_in_scope)}
Learning Objectives: {", ".join(ctx.learning_objectives)}
Difficulty: {ctx.difficulty}
Category: {ctx.category}

Output ONLY the JSON object. No other text.
"""

    def generate_pbq(self, ctx: PBQContext, pbq_id: str) -> Optional[PBQ]:
        prompt = self.build_prompt(ctx)

        for attempt in range(3):
            raw_output = self.llm.call(prompt)
            print("DEBUG raw_output:\n", raw_output[:2000])

            try:
                json_str = extract_last_json_block(raw_output)
            except Exception as e:
                if attempt < 2:
                    print(f"[Retry {attempt + 1}/2] JSON error: {e}\n")
                    continue
                print("❗ WARNING: All retries failed for this PBQ.")
                return None

            try:
                data = json.loads(json_str)
                print("DEBUG parsed JSON keys:", list(data.keys()))

                return PBQ(
                    id=pbq_id,
                    scenario_id=ctx.scenario_id,
                    difficulty=ctx.difficulty,
                    title=data["title"],
                    stem=data["stem"],
                    exhibits=[PBQExhibit(**ex) for ex in data.get("exhibits", [])],
                    tasks=[
                        PBQTask(
                            id=t["id"],
                            type=t["type"],
                            prompt=t["prompt"],
                            options=[PBQTaskOption(**opt) for opt in t["options"]],
                            correct_options=t["correct_options"],
                            rationale=t["rationale"],
                        )
                        for t in data.get("tasks", [])
                    ],
                )

            except Exception as e:
                if attempt < 2:
                    print(f"[Retry {attempt + 1}/2] JSON parse error: {e}\n")
                    continue
                print("❗ WARNING: All retries failed for this PBQ.")
                return None

        return None

