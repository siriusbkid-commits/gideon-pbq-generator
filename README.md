# gideon-pbq-generator
“Agentic AI that transforms IAM scenarios into exam‑ready PBQs.”

Agentic AI system that generates exam‑quality Performance‑Based Questions (PBQs) from IAM and cybersecurity scenarios.
Gideon — Agentic PBQ Generator for IAM & Cybersecurity
Gideon is an agentic AI system that autonomously generates exam‑quality Performance‑Based Questions (PBQs) from structured IAM and cybersecurity scenarios.
It interprets scenario JSON, builds a reasoning context, and produces validated PBQ output in both JSON and Markdown formats.

Designed for students, instructors, and cybersecurity practitioners, Gideon provides:

Multi‑stage autonomous reasoning

Scenario‑driven PBQ generation

Student Mode / Instructor Mode

Batch generation support

Deterministic offline model compatibility (Ollama)

Groq API support for high‑speed generation

Structured JSON validation and retry logic

Gideon turns simple scenario files into fully‑formed PBQs that mirror real exam formats used in IAM, identity governance, and security certifications.

Why Gideon?

Traditional PBQ creation is slow, manual, and inconsistent.
Gideon automates the entire process:

Reads scenario JSON

Builds a structured PBQ context

Generates tasks, exhibits, distractors, and rationales

Validates JSON output

Retries on failure

Saves clean PBQ files to pbq_output/

This makes it ideal for:

Cybersecurity students

Instructors building labs

⭐ 🙌 Acknowledgements

This project was created as a collaborative learning journey using the free version of Microsoft Copilot and a basic, low‑spec home computer. The goal is to show that anyone — regardless of budget or hardware — can build meaningful cybersecurity tools with curiosity, persistence, and creativity.

Special thanks to Microsoft Copilot for assisting with architecture, code generation, debugging, and educational design throughout the development of Gideon.

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
Runs entirely on your machine using Ollama + Phi‑3.

Installation
1. Install Python 3.10+
2. Install Ollama
https://ollama.com

3. Pull the Phi‑3 model
Code
ollama pull phi3:mini-instruct
4. Install Python dependencies
Code
pip install -r requirements.txt
Usage
Start Gideon:
Code
python Start.py
Menu Options:
Run scenarios

Generate PBQs

Batch PBQ mode

Toggle Student Mode

Exit

Output
PBQs are saved to:

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
Microsoft Copilot (free version) — architectural guidance, code generation, debugging, and educational design.
IAM practitioners

Certification prep

Training platforms

Automated content generation pipelines
