import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional


# ============================================================
# PBQ DATA MODELS
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

    def to_json(self) -> dict:
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
                    "options": [o.__dict__ for o in t.options],
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
    actors: list
    systems: list
    risks_findings: list
    controls_in_scope: list
    learning_objectives: list
    difficulty: str
    category: str


# ============================================================
# PBQ GENERATOR
# ============================================================

class PBQGenerator:
    def __init__(self, llm):
        self.llm = llm

    # ----------------------------------------------------------
    # STEP 1: Strip ANSI escape sequences (cursor movement, color codes)
    # ----------------------------------------------------------
    def _strip_ansi(self, text: str) -> str:
        # Single-line raw string — safe on all platforms
        return re.sub(r"\033\[[0-?]*[ -/]*[@-~]", "", text)

    # ----------------------------------------------------------
    # STEP 2: Strip ASCII control characters (except \t \n \r)
    # ----------------------------------------------------------
    def _strip_control_chars(self, text: str) -> str:
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

    # ----------------------------------------------------------
    # STEP 3: Remove markdown fences and extract outermost JSON block
    # ----------------------------------------------------------
    def _extract_json_block(self, text: str) -> str:
        if not text:
            raise ValueError("Empty input to JSON extractor.")

        # Strip markdown fences
        cleaned = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

        # Find the FIRST { and walk forward to find its matching }
        # This ensures we get the outermost object, not a nested rationale block
        start = cleaned.find("{")
        if start == -1:
            raise ValueError("No JSON object found in LLM output.")

        brace_count = 0
        in_string = False
        i = start

        while i < len(cleaned):
            ch = cleaned[i]

            if ch == '"' and (i == 0 or cleaned[i - 1] != "\\"):
                in_string = not in_string

            if not in_string:
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1

                if brace_count == 0:
                    return cleaned[start:i + 1]

            i += 1

        raise ValueError("No valid JSON object found — unmatched braces.")

    # ----------------------------------------------------------
    # STEP 4: Fix raw newlines inside quoted string values
    # Character-by-character to avoid regex multiline edge cases
    # ----------------------------------------------------------
    def _fix_newlines_in_strings(self, text: str) -> str:
        result = []
        in_string = False
        i = 0

        while i < len(text):
            ch = text[i]

            if ch == '"' and (i == 0 or text[i - 1] != "\\"):
                in_string = not in_string
                result.append(ch)
            elif ch in ("\n", "\r") and in_string:
                result.append(" ")
            else:
                result.append(ch)

            i += 1

        return "".join(result)

    # ----------------------------------------------------------
    # BUILD PROMPT
    # ----------------------------------------------------------
    def _build_prompt(self, ctx: PBQContext) -> str:
        return (
            "You are generating a PBQ (Performance-Based Question) for cybersecurity training.\n\n"
            "Return ONLY a single valid JSON object. No markdown. No backticks. No explanation.\n\n"
            "The JSON MUST have exactly these top-level keys:\n"
            '  "title", "stem", "exhibits", "tasks"\n\n'
            "title format: \"PBQ: " + ctx.title + "\"\n\n"
            "Each task MUST have:\n"
            '  "id", "type", "prompt", "options", "correct_options", "rationale"\n\n'
            "rationale MUST be a JSON object keyed by option id — NOT a plain string.\n"
            'Correct:   "rationale": {"a": "Why a is correct.", "b": "Why b is wrong."}\n'
            'Incorrect: "rationale": "Option a is correct because..."\n\n'
            "Each option MUST have: \"id\", \"text\"\n\n"
            "Each exhibit MUST have: \"id\", \"type\", \"label\", \"content\"\n\n"
            "CONTEXT:\n"
            f"Scenario ID: {ctx.scenario_id}\n"
            f"Title: {ctx.title}\n"
            f"Summary: {ctx.summary}\n"
            f"Actors: {', '.join(ctx.actors)}\n"
            f"Systems: {', '.join(ctx.systems)}\n"
            f"Risks: {', '.join(ctx.risks_findings)}\n"
            f"Controls: {', '.join(ctx.controls_in_scope)}\n"
            f"Learning Objectives: {', '.join(ctx.learning_objectives)}\n"
            f"Difficulty: {ctx.difficulty}\n"
            f"Category: {ctx.category}\n\n"
            "Output ONLY the JSON object."
        )

    # ----------------------------------------------------------
    # MAIN GENERATION WITH RETRY
    # ----------------------------------------------------------
    def generate_pbq(self, ctx: PBQContext, pbq_id: str) -> Optional[PBQ]:
        prompt = self._build_prompt(ctx)

        for attempt in range(3):
            raw = self.llm.call(prompt)
            print(f"\nDEBUG raw_output (attempt {attempt + 1}):\n{raw}\n")

            try:
                # Clean pipeline — order matters
                cleaned = self._strip_ansi(raw)
                cleaned = self._strip_control_chars(cleaned)
                cleaned = self._extract_json_block(cleaned)
                cleaned = self._fix_newlines_in_strings(cleaned)

                data = json.loads(cleaned)
                print("DEBUG parsed JSON keys:", list(data.keys()))

            except Exception as e:
                print(f"[Attempt {attempt + 1}/3] Parse error: {e}")
                if attempt < 2:
                    continue
                print("WARNING: All attempts failed.")
                return None

            # --------------------------------------------------
            # BUILD EXHIBITS
            # --------------------------------------------------
            exhibits = []
            for i, ex in enumerate(data.get("exhibits", [])):
                if isinstance(ex, str):
                    exhibits.append(PBQExhibit(
                        id=f"ex{i + 1}",
                        type="text",
                        label=f"Exhibit {i + 1}",
                        content=ex
                    ))
                elif isinstance(ex, dict):
                    exhibits.append(PBQExhibit(
                        id=ex.get("id", f"ex{i + 1}"),
                        type=ex.get("type", "text"),
                        label=ex.get("label", f"Exhibit {i + 1}"),
                        content=ex.get("content", ex.get("description", ""))
                    ))

            # Fallback exhibit if none provided
            if not exhibits:
                exhibits = [
                    PBQExhibit(id="ex1", type="text", label="Session Overview",
                               content="Review the privileged session timeline and connection metadata."),
                    PBQExhibit(id="ex2", type="text", label="Activity Log",
                               content="Review suspicious commands or PowerShell activity from the session."),
                ]

            # --------------------------------------------------
            # BUILD TASKS
            # --------------------------------------------------
            tasks = []
            for i, t in enumerate(data.get("tasks", [])):
                if not isinstance(t, dict):
                    continue

                options = [
                    PBQTaskOption(id=o["id"], text=o["text"])
                    for o in t.get("options", [])
                    if isinstance(o, dict) and "id" in o and "text" in o
                ]

                raw_rationale = t.get("rationale", {})
                if isinstance(raw_rationale, dict):
                    rationale = raw_rationale
                elif isinstance(raw_rationale, str) and raw_rationale.strip():
                    rationale = {"note": raw_rationale}
                else:
                    rationale = {}

                tasks.append(PBQTask(
                    id=t.get("id", f"task{i + 1}"),
                    type=t.get("type", "multiple_choice"),
                    prompt=t.get("prompt", t.get("title", t.get("description", f"Task {i + 1}"))),
                    options=options,
                    correct_options=t.get("correct_options", []),
                    rationale=rationale
                ))

            # Fallback tasks if none provided
            if not tasks:
                tasks = [
                    PBQTask(id="task1", type="multiple_choice",
                            prompt="Identify any privileged access policy violations.",
                            options=[], correct_options=[], rationale={}),
                    PBQTask(id="task2", type="multiple_choice",
                            prompt="Determine whether the session was authorized or anomalous.",
                            options=[], correct_options=[], rationale={}),
                ]

            return PBQ(
                id=pbq_id,
                scenario_id=ctx.scenario_id,
                difficulty=ctx.difficulty,
                title=data.get("title", f"PBQ: {ctx.title}"),
                stem=data.get("stem", ctx.summary),
                exhibits=exhibits,
                tasks=tasks
            )

        return None
