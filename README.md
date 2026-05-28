# GIDEON — Identity Attack Simulator

**GIDEON** is an open source, offline AI-powered simulator for generating Performance-Based Questions (PBQs) for Identity & Access Management (IAM) certification training.

Built for people studying certifications like **SC-300**, **CyberArk Defender**, **CISSP**, and other IAM-focused exams who couldn't find enough free, practical PBQ practice material.

---

## What is a PBQ?

A Performance-Based Question (PBQ) is a scenario-driven exam question that tests practical knowledge rather than simple recall. They appear in certifications like SC-300, CompTIA Security+, and CyberArk exams. They are expensive to produce and rarely available for free practice — GIDEON fixes that.

---

## Features

- Generate unlimited PBQs from scenario files
- Supports multiple IAM categories: SC-300, CyberArk Defender, IAM Fundamentals, Governance & Compliance
- Instructor mode (with answers and rationales) and Student mode (clean practice version)
- Outputs JSON and Markdown files for each PBQ
- Batch generation mode for producing multiple PBQs at once
- Fully offline — runs on a local Ollama LLM, no API keys or internet required
- Scenario-driven — add your own `.json` scenario files to extend coverage

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- `mistral-nemo` model pulled in Ollama

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/gideon-iam-simulator.git
cd gideon-iam-simulator
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download and install Ollama from [https://ollama.com](https://ollama.com).

### 4. Pull the required model

```bash
ollama pull mistral-nemo
```

This is approximately a 7GB download. Once complete, confirm it works:

```bash
ollama run mistral-nemo "say hello"
```

---

## Usage

### Start the simulator

```bash
python start.py
```

You will see the main menu:

```
========================================
 GIDEON: Identity Attack Simulator
========================================

1. Run scenario → breach_admin_escalation.json
2. Run scenario → contractor_onboarding.json
3. Run scenario → cyberark_session_misuse.json
...
9. PBQ-Only Mode (Generate PBQ without IAM chain)
10. Batch PBQ Mode (Generate multiple PBQs)
11. Toggle Student Mode (Hide/Show Rationales)
```

### Menu options

| Option | Description |
|--------|-------------|
| 1–7 | Run a full IAM chain analysis + generate a PBQ for that scenario |
| 8 | Exit |
| 9 | Generate a PBQ directly without running the IAM chain |
| 10 | Batch generate multiple PBQs from a scenario |
| 11 | Toggle between Instructor mode (answers shown) and Student mode (answers hidden) |

### Output files

Each generated PBQ produces up to three files in the `output/` or `pbq_output/` folder:

- `pbq_[id]_[timestamp].json` — full structured PBQ data
- `pbq_[id]_[timestamp]_instructor.md` — Markdown with correct answers and rationales
- `pbq_[id]_[timestamp]_student.md` — Clean Markdown for practice (no answers)
- ## Viewing Your Output Files

Open any `.md` file in VS Code and press `Ctrl+Shift+V` 
to see the beautifully rendered markdown preview instead 
of raw text.

---

## Adding Scenarios

Scenarios are `.json` files in the `scenarios/` folder. Each scenario follows this structure:

```json
{
  "id": "your_scenario_id",
  "metadata": {
    "title": "Your Scenario Title",
    "summary": "A brief description of the scenario.",
    "actors": ["Actor 1", "Actor 2"],
    "systems": ["System 1", "System 2"],
    "risks": ["Risk 1", "Risk 2"],
    "controls": ["Control 1", "Control 2"],
    "learning_objectives": ["Objective 1", "Objective 2"],
    "difficulty": "medium",
    "category": "SC-300"
  }
}
```

Add your file to the `scenarios/` folder and it will appear in the menu automatically.

---

## Project Structure

```
gideon-iam-simulator/
├── scenarios/              # Scenario JSON files
├── pbq/
│   ├── __init__.py
│   ├── generator.py        # Core PBQ generation logic and data models
│   └── menu.py             # CLI menu helpers
├── utils/
│   └── save_pbq.py         # File saving helpers (JSON + Markdown)
├── output/                 # Generated PBQ outputs (gitignored)
├── pbq_output/             # PBQ-only mode outputs (gitignored)
├── start.py                # Main entry point
├── run_chained.py          # IAM chain + PBQ runner
├── llm_factory.py          # Ollama LLM wrapper
├── config.py               # Model and mode configuration
└── README.md
```

---

## Configuration

Edit `config.py` to change the model:

```python
LOCAL_MODEL = "mistral-nemo"  # Change to any Ollama model
```

---

## Forking and Contributing

This project is open source and built to be forked and extended. Some ideas for contributions:

- Add new scenario files for different certification domains
- Add support for drag-and-drop or matching question types
- Build a web UI for the simulator
- Add scoring and progress tracking
- Support additional LLM backends

Pull requests are welcome!

---

## Why GIDEON?

PBQ practice material is either paywalled, scarce, or outdated. This project was built out of frustration while studying for IAM certifications and not being able to find enough free, practical scenario-based questions. GIDEON generates unlimited, scenario-specific PBQs locally with no cost and no internet connection required.

---

## License

MIT License — free to use, modify, and distribute.

---

## Disclaimer

Generated PBQs are AI-produced and intended for study purposes only. Always verify answers against official certification documentation and study materials.


This project was created as a collaborative learning journey using the free version of Microsoft Copilot and a basic, low‑spec home computer. The goal is to show that anyone — regardless of budget or hardware — can build meaningful cybersecurity tools with curiosity, persistence, and creativity.

Special thanks to Microsoft Copilot & Claude for assisting with architecture, code generation, debugging, and educational design throughout the development of Gideon.

⭐ 🌱 Project Philosophy
Gideon was built on a simple belief:

Cybersecurity education should be accessible, practical, and empowering — not locked behind expensive tools or enterprise environments.

This project exists to help students, career‑changers, and curious learners understand identity attacks, privileged access, and PBQ‑style thinking through hands‑on, scenario‑driven learning.

Gideon is not just a tool — it’s a statement:

You can learn cybersecurity without enterprise access

You can build real tools without a powerful machine

You can create value with free AI

You can grow through experimentation, not perfection

⭐ 🌍 Why Open Source?
Gideon is open source because:

Learning grows faster when shared

Transparency builds trust

Community improves quality

Students deserve tools they can modify and extend

Cybersecurity benefits from collaboration, not gatekeeping

Anyone can fork, remix, extend, or adapt Gideon for:

teaching

labs

PBQ practice

scenario design

identity engineering demos

personal learning

Open source means Gideon belongs to everyone — not just one person.

Development Hardware
Gideon was built entirely on a low‑spec, everyday home laptop, proving that meaningful cybersecurity tools don’t require expensive hardware or enterprise‑grade machines.

Development machine:

Model: HP 15‑fd0xxx

CPU: 12th/13th‑gen Intel mobile processor

RAM: 16 GB

GPU: Integrated graphics

OS: Windows 11 Home

Editor: Micro (terminal‑based)

AI Assistant: Free version of Microsoft Copilot

This project demonstrates that curiosity, persistence, and creativity matter far more than hardware.



Many students believe they need a powerful workstation or expensive tools to start learning cybersecurity or building projects. Gideon was intentionally developed on modest hardware to show that you can start exactly where you are, with what you have.

⭐ 🤝 How to Contribute
Contributions of all kinds are welcome:

New scenarios

New PBQ categories

Improvements to the menu system

Better error handling

UI enhancements

Documentation improvements

Bug fixes

Feature ideas

To contribute:

Fork the repository

Create a new branch

Make your changes

Submit a pull request

Even small contributions help the project grow.
GIDEON: Identity Attack Simulator & PBQ Generator
Gideon is an open‑source Identity & Access Management (IAM) attack simulator and PBQ (Performance‑Based Question) generator designed for:

SC‑300 (Microsoft Identity)

CyberArk Defender

IAM fundamentals

Governance & compliance

Privileged access investigations

Security training & labs

Gideon generates realistic IAM scenarios, then produces PBQs with:

stems

exhibits

tasks

options

correct answers

rationales (optional Student Mode)

It can run:

single scenarios

PBQ‑only mode

batch PBQ generation

student/instructor modes

Features
✔ IAM Attack Simulator
Run realistic identity breach scenarios:

Admin privilege escalation

MFA fatigue attacks

PIM emergency access

CyberArk PSM session misuse

Contractor onboarding

Privileged access reviews

✔ PBQ Generator
Create exam‑style PBQs with:

JSON output

Markdown output

Exhibits

Multi‑task questions

Hidden rationales (Student Mode)

✔ Batch PBQ Mode
Generate 5, 10, 20+ PBQs at once.

✔ Student / Instructor Mode
Student Mode hides rationales

Instructor Mode shows full explanations

✔ Fully Local

Code
output/pbq_output/
output/batch_pbq/
Both JSON and Markdown formats are supported.

Roadmap
Okta IAM scenarios

AWS IAM scenarios

GCP IAM scenarios

SailPoint governance scenarios

Web UI dashboard

PBQ difficulty tuning

Multi‑exhibit PBQs

Log‑rich investigations


⭐ 👤 Credits
Created by:  
John Pickering  
Identity & Access Management Student
CyberArk Defender Candidate
Creator of the Gideon PBQ Generator

AI Collaboration:  
Microsoft Copilot & Claude (free versions) — architectural guidance, code generation, debugging, and educational design.
IAM practitioners

Certification prep

Training platforms

Automated content generation pipelines
