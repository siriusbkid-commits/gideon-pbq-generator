# GIDEON - Free AI-Powered Cybersecurity Scenario Generator

GIDEON is a free open source tool that generates unlimited cybersecurity practice scenarios across multiple domains. Used by students, IT professionals, SOC analysts, OT/ICS engineers and IoT security practitioners worldwide.

No subscription. No API key. Runs locally on your machine.

## What GIDEON Generates

### IAM Chain Scenarios (Options 1-7)

Full Identity and Access Management attack chain simulations powered by a local AI model. Each scenario runs a complete IAM investigation and generates a Performance-Based Question (PBQ) with answers and rationales.

Scenarios include:

- Admin privilege escalation via breach
- MFA fatigue attacks
- CyberArk PSM session misuse
- Contractor onboarding security review
- PIM emergency access investigation
- Privileged access review
- Conditional access policy analysis

Supported exam categories: SC-300, CyberArk Defender, IAM Fundamentals, Governance and Compliance, Vendor-Neutral IAM

### PBQ-Only Mode (Option 9)

Generate a single PBQ directly from any scenario file without running the full IAM chain. Faster generation for focused exam practice.

### Batch PBQ Mode (Option 10)

Generate 5, 10, 20 or more PBQs at once from any scenario file. All saved as JSON and Markdown files in your output folder.

### CySA+ CS0-004 PBQ Mode (Option 12)

Open-ended scenario-based questions across all four CS0-004 domains. No LLM required - instant generation:

- Domain 1: Security Operations (34%)
- Domain 2: Vulnerability Management (26%)
- Domain 3: Incident Response and Management (24%)
- Domain 4: Reporting and Communication (16%)

### CySA+ CS0-004 Log Analysis Mode (Option 13)

Realistic log scenarios with open-ended questions covering:

- Windows Security Event Logs
- Firewall and Network Logs
- DNS Logs
- Authentication and IAM Logs
- IDS/IPS Logs
- Web Server and Application Logs

### OT/ICS Security Scenarios (Option 14)

Industrial Control Systems security scenarios for IT professionals. No LLM required - instant generation:

- OT/ICS Architecture and Purdue Model
- Threat Landscape (Nation-state, Ransomware, Supply Chain)
- Defensive Controls (IEC 62443, NIST SP 800-82)
- Incident Response in OT Environments

Frameworks: IEC 62443, NIST SP 800-82, MITRE ATT&CK for ICS

### IoT Security Scenarios (Option 15)

Internet of Things security scenarios covering:

- IoT Architecture and Attack Surface
- OWASP IoT Top 10
- IoT Network Security
- Industrial IoT (IIoT)
- IoT Incident Response
- AI and Emerging Threats

Frameworks: OWASP IoT Top 10, NIST SP 800-213, ENISA IoT Guidelines

### SC-300 PBQ Mode (Option 16)

Dedicated Microsoft Identity and Access Administrator exam practice. No LLM required - instant generation. Covers all four SC-300 domains with randomised variables for unique scenarios every time:

- Domain 1: Implement and Manage User Identities (20-25%)
- Domain 2: Implement Authentication and Access Management (25-30%)
- Domain 3: Plan and Implement Workload Identities (20-25%)
- Domain 4: Plan and Automate Identity Governance (20-25%)

### CyberArk Defender PAM-DEF PBQ Mode (Option 17)

Dedicated CyberArk Defender PAM (PAM-DEF) exam practice. No LLM required - instant generation. Covers all seven official PAM-DEF knowledge domains:

- Domain 1: Account Onboarding (~15%)
- Domain 2: Application Management (~10%)
- Domain 3: Ongoing Maintenance (~15%)
- Domain 4: Password Management Configuration (~15%)
- Domain 5: Security and Audit (~15%)
- Domain 6: Session Management Configuration (~20%)
- Domain 7: User Management Configuration (~10%)

## Complete Menu Reference

| Option | Description | Requires LLM |
|--------|-------------|--------------|
| 1-7 | Run full IAM chain scenarios | Yes - Ollama mistral-nemo |
| 8 | Exit | - |
| 9 | PBQ-Only Mode | Yes - Ollama mistral-nemo |
| 10 | Batch PBQ Mode | Yes - Ollama mistral-nemo |
| 11 | Toggle Student/Instructor Mode | - |
| 12 | CySA+ CS0-004 PBQ Mode | No - instant |
| 13 | CySA+ Log Analysis Mode | No - instant |
| 14 | OT/ICS Security Scenarios | No - instant |
| 15 | IoT Security Scenarios | No - instant |
| 16 | SC-300 PBQ Mode (Microsoft Identity and Access Administrator) | No - instant |
| 17 | CyberArk Defender PAM-DEF PBQ Mode (Privileged Access Management) | No - instant |

## Supported Topics

| Module | Templates | Exam/Standard | Mode |
|--------|-----------|---------------|------|
| SC-300 IAM Chain Scenarios | 7 | SC-300 / CyberArk | LLM Required |
| SC-300 Dedicated PBQ Mode | 15 | SC-300 Microsoft Identity Administrator | Instant |
| CySA+ CS0-004 PBQ | 13 | CompTIA CS0-004 | Instant |
| Log Analysis | 11 | CompTIA CS0-004 | Instant |
| OT/ICS Security | 13 | IEC 62443 / NIST SP 800-82 | Instant |
| IoT Security | 12 | OWASP IoT Top 10 / NIST SP 800-213 | Instant |
| CyberArk Defender PAM-DEF | 11 | CyberArk PAM-DEF | Instant |

## Quick Start

git clone https://github.com/siriusbkid-commits/gideon-pbq-generator.git
cd gideon-pbq-generator
python start.py

For options 12-17 no additional setup is needed - just clone and run.

For options 1-11 you also need Ollama installed with mistral-nemo:

1. Download Ollama from https://ollama.com
2. Run: ollama pull mistral-nemo
3. Run: ollama serve

## Requirements

- Python 3.10+
- No external dependencies for options 12-17
- Ollama with mistral-nemo (7GB download) for options 1-11

## Student and Instructor Mode

Toggle between modes using Option 11:

- Student Mode: scenarios and questions only - no answers shown
- Instructor Mode: full model answers and rationales shown

## Output Files

Each generated PBQ saves to your output folder:

- JSON file: structured PBQ data
- Markdown file: formatted for reading in VS Code

Open .md files in VS Code and press Ctrl+Shift+V for rendered preview.

## Who Is GIDEON For?

- SC-300 Microsoft Identity and Access Administrator exam candidates
- CyberArk Defender PAM-DEF exam candidates
- CySA+ CS0-004 exam candidates
- OT/ICS security professionals and students
- IoT security researchers and practitioners
- SOC analysts building scenario analysis skills
- IT professionals transitioning into OT/ICS or IoT security roles
- Cybersecurity instructors running training programmes

## Pair With the Full Udemy Courses

### CySA+ CS0-004
- CySA+ Log Mastery: Practice Tests for CS0-004 https://www.udemy.com/course/cysa-log-mastery-practice-tests-for-cs0-004
- GIDEON: Generate Unlimited SC-300 and CyberArk PBQs for Free https://www.udemy.com/course/pbq-generator-mastery-create-iam-sc300-practice-pbqs

### OT/ICS Security
- OT/ICS Security Practice Tests for IT Professionals https://www.udemy.com/course/otics-security-practice-tests-for-it-professionals

### IoT Security
- IoT Security Practice Tests for IT Professionals https://www.udemy.com/course/iot-security-practice-tests-for-it-professionals

## Free Study Resources

### SC-300 Microsoft Identity Administrator
- Microsoft SC-300 Exam Page: https://learn.microsoft.com/credentials/certifications/exams/sc-300
- Microsoft Entra ID Documentation: https://learn.microsoft.com/entra/identity/
- Microsoft Learn SC-300 Study Guide: https://learn.microsoft.com/credentials/certifications/identity-and-access-administrator/

### CyberArk Defender PAM-DEF
- CyberArk Certification Page: https://www.cyberark.com/services-support/training-certification/
- CyberArk Documentation Portal: https://docs.cyberark.com
- CyberArk PAM Administration Training: https://training.cyberark.com

### OT/ICS Security
- NIST SP 800-82: https://csrc.nist.gov/publications/detail/sp/800-82/rev-3/final
- MITRE ATT&CK for ICS: https://attack.mitre.org/matrices/ics/
- CISA ICS Advisories: https://www.cisa.gov/ics-advisories

### IoT Security
- OWASP IoT Top 10: https://owasp.org/www-project-internet-of-things/
- NIST SP 800-213: https://csrc.nist.gov/publications/detail/sp/800-213/final
- ENISA IoT Guidelines: https://www.enisa.europa.eu/topics/iot-and-smart-infrastructure

### CySA+ CS0-004
- CompTIA CySA+ Exam Objectives: https://www.comptia.org/certifications/cybersecurity-analyst
- MITRE ATT&CK Framework: https://attack.mitre.org

## Adding Your Own Scenarios

Add custom .json scenario files to the scenarios/ folder and they appear in the menu automatically. See examples/ for the scenario file format.

## Roadmap

### Currently Available

- SC-300 - Microsoft Identity Administrator scenarios (LLM chain + dedicated instant PBQ mode)
- CyberArk Defender PAM-DEF - dedicated instant PBQ mode across all 7 domains
- CySA+ CS0-004 - PBQ and log analysis scenarios
- OT/ICS Security - 120 practice questions
- IoT Security - 120 practice questions + AI scenarios

### Coming Soon

- CompTIA SecOT+ - OT security scenarios (launching December 2026)
- CompTIA SecurityAI+ - AI security scenarios
- NZ Health Security - HISO 10029.1 compliance scenarios and clinical IAM PBQs
- SC-500 - Microsoft Cloud and AI Security scenarios

## Community Contributions Welcome

Add your own scenario packs - see Adding Your Own Scenarios above.

## About

Built by John Pickering as a free companion tool for cybersecurity students and professionals worldwide.

Star this repo if you find it useful - it helps other students find it!
