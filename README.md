# GIDEON - Free AI-Powered Cybersecurity Scenario Generator

GIDEON is a free open source tool that generates unlimited cybersecurity
practice scenarios across multiple domains. Used by students, IT professionals,
SOC analysts, OT/ICS engineers and IoT security practitioners worldwide.

No subscription. No API key. Runs locally on your machine.

## What GIDEON Generates

### Option 12 - CySA+ CS0-004 PBQ Mode
Open-ended scenario-based questions across all four CS0-004 domains:
- Domain 1: Security Operations (34%)
- Domain 2: Vulnerability Management (26%)
- Domain 3: Incident Response and Management (24%)
- Domain 4: Reporting and Communication (16%)

### Option 13 - CySA+ CS0-004 Log Analysis Mode
Realistic log scenarios with open-ended questions covering:
- Windows Security Event Logs
- Firewall and Network Logs
- DNS Logs
- Authentication and IAM Logs
- IDS/IPS Logs
- Web Server and Application Logs

### Option 14 - OT/ICS Security Scenarios
Industrial Control Systems security scenarios for IT professionals:
- OT/ICS Architecture and Purdue Model
- Threat Landscape (Nation-state, Ransomware, Supply Chain)
- Defensive Controls (IEC 62443, NIST SP 800-82)
- Incident Response in OT Environments
Frameworks: IEC 62443, NIST SP 800-82, MITRE ATT&CK for ICS

### Option 15 - IoT Security Scenarios
Internet of Things security scenarios covering:
- IoT Architecture and Attack Surface
- OWASP IoT Top 10
- IoT Network Security
- Industrial IoT (IIoT)
- IoT Incident Response
Frameworks: OWASP IoT Top 10, NIST SP 800-213, ENISA IoT Guidelines

Every scenario uses randomised variables so you get a unique scenario every time.
Hundreds of unique combinations from 46 scenario templates.

## Supported Topics

| Module | Templates | Exam/Standard | Mode |
|--------|-----------|---------------|------|
| CySA+ CS0-004 PBQ | 13 | CompTIA CS0-004 | Exam Prep |
| Log Analysis | 11 | CompTIA CS0-004 | Exam Prep |
| OT/ICS Security | 13 | IEC 62443 / NIST SP 800-82 | Standalone |
| IoT Security | 9 | OWASP IoT Top 10 / NIST SP 800-213 | Standalone |

## Quick Start

git clone https://github.com/siriusbkid-commits/gideon-pbq-generator.git
cd gideon-pbq-generator
python start.py

Then select from the menu:
- Option 12 - CySA+ CS0-004 PBQ Mode
- Option 13 - CySA+ CS0-004 Log Analysis Mode
- Option 14 - OT/ICS Security Scenarios
- Option 15 - IoT Security Scenarios

## Requirements

- Python 3.10+
- No external dependencies for options 12-15 - runs instantly with no LLM required
- Ollama with mistral-nemo required for options 1-11 (IAM scenarios)

## Who Is GIDEON For?

- CySA+ CS0-004 exam candidates
- OT/ICS security professionals and students
- IoT security researchers and practitioners
- SOC analysts building scenario analysis skills
- IT professionals transitioning into OT/ICS or IoT security roles
- Instructors running cybersecurity training programmes

## Pair With the Full Udemy Courses

GIDEON pairs perfectly with these Udemy courses:

### CySA+ CS0-004
- CySA+ Log Mastery: Practice Tests for CS0-004
  ADD YOUR UDEMY URL HERE
- GIDEON: Generate Unlimited SC-300 and CyberArk PBQs for Free
  ADD YOUR UDEMY URL HERE

### OT/ICS Security
- OT/ICS Security for IT Professionals
  COMING SOON

### IoT Security
- IoT Security for IT Professionals
  COMING SOON

## How the Free Tool and Paid Courses Work Together

| Tool | Format | Best For |
|------|--------|----------|
| GIDEON (free) | Open-ended scenarios | Building deep practical skills |
| Udemy courses (paid) | Guided learning with explanations | Structured learning and exam prep |

Use GIDEON to build the skill. Use the Udemy courses to structure the knowledge.

## Free Study Resources

### OT/ICS Security
- NIST SP 800-82: https://csrc.nist.gov/publications/detail/sp/800-82/rev-3/final
- MITRE ATT&CK for ICS: https://attack.mitre.org/matrices/ics/
- CISA ICS Advisories: https://www.cisa.gov/ics-advisories

### IoT Security
- OWASP IoT Top 10: https://owasp.org/www-project-internet-of-things/
- NIST SP 800-213: https://csrc.nist.gov/publications/detail/sp/800-213/final
- ENISA IoT Guidelines: https://www.enisa.europa.eu/topics/iot-and-smart-infrastructure

## About

Built by John Pickering as a free companion tool for cybersecurity students
and professionals worldwide.

Star this repo if you find it useful - it helps other students find it!
