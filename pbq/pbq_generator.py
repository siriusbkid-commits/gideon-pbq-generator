import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


# ============================================================
# Data Models
# ============================================================

@dataclass
class Exhibit:
    id: str
    type: str
    label: str
    content: str


@dataclass
class Option:
    id: str
    text: str


@dataclass
class Task:
    id: str
    type: str
    prompt: str
    options: List[Option]
    correct_options: List[str]
    rationale: Dict[str, str]


@dataclass
class PBQ:
    id: str
    scenario_id: str
    title: str
    stem: str
    exhibits: List[Exhibit]
    tasks: List[Task]
    difficulty: str
    category: str

    # --------------------------------------------------------
    # JSON Export
    # --------------------------------------------------------
    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "title": self.title,
            "stem": self.stem,
            "exhibits": [asdict(e) for e in self.exhibits],
            "tasks": [
                {
                    "id": t.id,
                    "type": t.type,
                    "prompt": t.prompt,
                    "options": [asdict(o) for o in t.options],
                    "correct_options": t.correct_options,
                    "rationale": t.rationale,
                }
                for t in self.tasks
            ],
            "difficulty": self.difficulty,
            "category": self.category,
        }

    # --------------------------------------------------------
    # Instructor Markdown (answers + rationales)
    # --------------------------------------------------------
    def to_markdown_instructor(self) -> str:
        lines: List[str] = []

        lines.append(f"# {self.title}\n")

        lines.append("## Metadata")
        lines.append(f"- **Scenario ID:** {self.scenario_id}")
        lines.append(f"- **Difficulty:** {self.difficulty}")
        lines.append(f"- **Category:** {self.category}")
        lines.append("")

        lines.append("## Scenario")
        lines.append(self.stem.strip() + "\n")

        if self.exhibits:
            lines.append("## Exhibits")
            for ex in self.exhibits:
                lines.append(f"### {ex.label}")
                lines.append(f"**Type:** {ex.type}")
                lines.append("")
                lines.append(ex.content.strip())
                lines.append("")
            lines.append("")

        lines.append("## Tasks")
        for t in self.tasks:
            lines.append(f"### Task {t.id}: {t.prompt}")
            lines.append("")

            if t.options:
                lines.append("**Options:**")
                for opt in t.options:
                    lines.append(f"- **{opt.id}.** {opt.text}")
                lines.append("")

            if t.correct_options:
                lines.append(f"**Correct Answer(s):** {', '.join(t.correct_options)}")
                lines.append("")

            if t.rationale:
                lines.append("**Rationale:**")
                for key, value in t.rationale.items():
                    lines.append(f"- **{key}** — {value}")
                lines.append("")

            lines.append("---\n")

        return "\n".join(lines)

    # --------------------------------------------------------
    # Student Markdown (no answers, no rationales)
    # --------------------------------------------------------
    def to_markdown_student(self) -> str:
        lines: List[str] = []

        lines.append(f"# {self.title}\n")

        lines.append("## Scenario")
        lines.append(self.stem.strip() + "\n")

        if self.exhibits:
            lines.append("## Exhibits")
            for ex in self.exhibits:
                lines.append(f"### {ex.label}")
                lines.append(f"**Type:** {ex.type}")
                lines.append("")
                lines.append(ex.content.strip())
                lines.append("")
            lines.append("")

        lines.append("## Tasks")
        for t in self.tasks:
            lines.append(f"### Task {t.id}: {t.prompt}")
            lines.append("")

            if t.options:
                lines.append("**Options:**")
                for opt in t.options:
                    lines.append(f"- [ ] **{opt.id}.** {opt.text}")
                lines.append("")

            lines.append("---\n")

        return "\n".join(lines)


# ============================================================
# PBQ Context
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
# PBQ Generator
# ============================================================

class PBQGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    # --------------------------------------------------------
    # Strict Prompt Builder
    # --------------------------------------------------------
    def build_prompt(self, ctx: PBQContext) -> str:
        return f"""
You are generating a Performance-Based Question (PBQ) for IAM training.

STRICT RULES — DO NOT BREAK THESE:
- Output MUST be valid JSON.
- DO NOT include HTML, <img>, <iframe>, <table>, or any markup.
- DO NOT include URLs.
- DO NOT include markdown inside JSON.
- DO NOT include line breaks inside JSON strings.
- DO NOT include floating-point numbers (e.g., 1.1). Use integers or single-letter IDs only.
- DO NOT include keys without quotes.
- DO NOT include trailing commas.
- Exhibits MUST be plain text only.
- Options MUST be plain text only.
- Rationale MUST be plain text only.
- Rationale MUST be a JSON object keyed by option id — NOT a plain string.
- Correct: "rationale": {{"a": "Why a is correct.", "b": "Why b is wrong."}}
- Incorrect: "rationale": "Option a is correct because..."

Your JSON MUST follow this exact schema:

{{
  "title": "string",
  "stem": "string",
  "exhibits": [
    {{
      "id": "e1",
      "type": "text",
      "label": "string",
      "content": "string"
    }}
  ],
  "tasks": [
    {{
      "id": "t1",
      "type": "identify|analyze|evaluate|apply|recall|interpret",
      "prompt": "string",
      "options": [
        {{"id": "a", "text": "string"}},
        {{"id": "b", "text": "string"}}
      ],
      "correct_options": ["a"],
      "rationale": {{
        "a": "string",
        "b": "string"
      }}
    }}
  ]
}}

CONTENT REQUIREMENTS:
- Title: short, exam-style.
- Stem: 2-4 sentences describing the scenario.
- Exhibits: 1-2 short text exhibits (no images, no HTML, no URLs).
- Tasks: 3-4 tasks.
- Options: 2-4 per task.
- Correct options: 1-2 per task.
- Rationale: 1-2 sentences per option.

CONTEXT FOR THIS PBQ:
Scenario ID: {ctx.scenario_id}
Title: {ctx.title}
Summary: {ctx.summary}
Actors: {ctx.actors}
Systems: {ctx.systems}
Risks/Findings: {ctx.risks_findings}
Controls in Scope: {ctx.controls_in_scope}
Learning Objectives: {ctx.learning_objectives}
Difficulty: {ctx.difficulty}
Category: {ctx.category}

Now generate the PBQ JSON ONLY. No explanations. No commentary.
"""

    # --------------------------------------------------------
    # Core Generation
    # --------------------------------------------------------
    def generate_pbq(self, ctx: PBQContext, pbq_id: str, max_retries: int = 3) -> Optional["PBQ"]:
        prompt = self.build_prompt(ctx)

        for attempt in range(1, max_retries + 1):
            raw_output = self.llm_client.call(prompt)

            print(f"\nDEBUG raw_output (attempt {attempt}):")
            print(raw_output)
            print("\n")

            # Cleaning pipeline — order matters
            # 1. Strip ANSI escape sequences
            # 2. Fix LLM word-wrap artifacts (e.g. "compa company" -> "company")
            # 3. Strip control characters
            # 4. Strip markdown fences and normalize line endings
            # 5. Fix raw newlines inside JSON strings
            # 6. Extract the outermost JSON block
            cleaned = self._strip_ansi(raw_output)
            cleaned = self._fix_word_wrapping(cleaned)
            cleaned = self._strip_control_chars(cleaned)
            cleaned = self._normalize_json_whitespace(cleaned)
            cleaned = self._fix_newlines_in_strings(cleaned)
            json_str = self._extract_json_block(cleaned)

            if json_str is None:
                print(f"[Attempt {attempt}/{max_retries}] No JSON block found.")
                continue

            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"[Attempt {attempt}/{max_retries}] Parse error: {e}")
                continue

            try:
                pbq = self._build_pbq_from_dict(data, ctx, pbq_id)
                return pbq
            except Exception as e:
                print(f"[Attempt {attempt}/{max_retries}] Failed to build PBQ object: {e}")
                continue

        print("WARNING: All attempts failed.")
        return None

    # --------------------------------------------------------
    # Helpers: JSON Extraction & Cleaning
    # --------------------------------------------------------

    def _strip_ansi(self, text: str) -> str:
        # Single-line raw string — safe on all platforms including Windows
        return re.sub(r"\033\[[0-?]*[ -/]*[@-~]", "", text)

    def _fix_word_wrapping(self, text: str) -> str:
        """
        Fix LLM word-wrap artifacts where a word is split and repeated.
        e.g. 'compa company' -> 'company'
        e.g. 'named J John' -> 'named John'
        e.g. 'your your decision' -> 'your decision'
        """
        # Fix fully duplicated words: "your your" -> "your"
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
        # Fix partial-then-full word: "compa company" -> "company"
        text = re.sub(r'\b\w{2,}\s+(\w{4,})\b', lambda m: m.group(0) if m.group(0).split()[0] == m.group(1)[:len(m.group(0).split()[0])] else m.group(0), text)
        return text

    def _strip_control_chars(self, text: str) -> str:
        # Remove ASCII control chars except tab, newline, carriage return
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

    def _normalize_json_whitespace(self, s: str) -> str:
        """
        Remove markdown fences and normalize line endings.
        Must run before _fix_newlines_in_strings.
        """
        s = s.strip()

        if s.startswith("```"):
            s = re.sub(r"^```[a-zA-Z0-9]*", "", s)
            s = s.replace("```", "").strip()

        s = s.replace("\r\n", "\n")
        return s

    def _fix_newlines_in_strings(self, text: str) -> str:
        """
        Replace raw newlines inside JSON string values with a space.
        Character-by-character to reliably track string context.
        Must run BEFORE _extract_json_block.
        """
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

    def _extract_json_block(self, text: str) -> Optional[str]:
        """
        Extract the first top-level JSON object from the text.
        Tracks string context to avoid false brace matching.
        """
        start = text.find("{")
        if start == -1:
            return None

        depth = 0
        in_string = False
        i = start

        while i < len(text):
            ch = text[i]

            if ch == '"' and (i == 0 or text[i - 1] != "\\"):
                in_string = not in_string

            if not in_string:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start:i + 1]
            i += 1

        return None

    # --------------------------------------------------------
    # Helpers: Build PBQ Object
    # --------------------------------------------------------
    def _build_pbq_from_dict(self, data: Dict[str, Any], ctx: PBQContext, pbq_id: str) -> "PBQ":
        title = data.get("title", ctx.title)
        stem = data.get("stem", ctx.summary)

        exhibits: List[Exhibit] = []
        for ex in data.get("exhibits", []):
            exhibits.append(Exhibit(
                id=str(ex.get("id", "e1")),
                type=str(ex.get("type", "text")),
                label=str(ex.get("label", "Exhibit")),
                content=str(ex.get("content", ""))
            ))

        tasks: List[Task] = []
        for t in data.get("tasks", []):
            options: List[Option] = []
            for opt in t.get("options", []):
                options.append(Option(
                    id=str(opt.get("id", "a")),
                    text=str(opt.get("text", ""))
                ))

            correct_options = [str(c) for c in t.get("correct_options", [])]

            raw_rationale = t.get("rationale", {})
            if isinstance(raw_rationale, dict):
                rationale = {str(k): str(v) for k, v in raw_rationale.items()}
            elif isinstance(raw_rationale, str) and raw_rationale.strip():
                rationale = {"note": raw_rationale}
            else:
                rationale = {}

            tasks.append(Task(
                id=str(t.get("id", "t1")),
                type=str(t.get("type", "identify")),
                prompt=str(t.get("prompt", "")),
                options=options,
                correct_options=correct_options,
                rationale=rationale,
            ))

        return PBQ(
            id=pbq_id,
            scenario_id=ctx.scenario_id,
            title=title,
            stem=stem,
            exhibits=exhibits,
            tasks=tasks,
            difficulty=ctx.difficulty,
            category=ctx.category,
        )

