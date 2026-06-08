# GIDEON - Free AI-Powered PBQ and Log Analysis Generator

GIDEON is a free open source tool that generates unlimited Performance-Based Question (PBQ) scenarios and realistic log analysis practice scenarios for cybersecurity certification exam preparation.

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
- Firewall / Network Logs
- DNS Logs
- Authentication / IAM Logs
- IDS/IPS Logs
- Web Server / Application Logs

Every scenario uses randomised variables so you get a unique scenario every time.

## Supported Exams

| Exam | PBQ Mode | Log Analysis Mode |
|------|----------|-------------------|
| SC-300 (Microsoft Identity) | Yes | - |
| CyberArk Defender | Yes | - |
| CySA+ CS0-004 | Yes | Yes |

## Quick Start

git clone https://github.com/siriusbkid-commits/gideon-pbq-generator.git
cd gideon-pbq-generator
python start.py

Then select from the menu:
- Option 12 - CySA+ CS0-004 PBQ Mode
- Option 13 - CySA+ CS0-004 Log Analysis Mode

## Requirements

- Python 3.10+
- No external dependencies for CySA+ modes - runs instantly with no LLM required

## Pair With the Full Udemy Courses

GIDEON pairs perfectly with these Udemy courses for complete exam preparation:

### CySA+ CS0-004
- CySA+ Log Mastery: Practice Tests for CS0-004 - Mixed Log Analysis
  https://www.udemy.com/course/cysa-log-mastery-practice-tests-for-cs0-004
  100 multiple choice questions with full explanations across all 6 log types

- GIDEON: Generate Unlimited SC-300 and CyberArk PBQs for Free
 https://www.udemy.com/course/pbq-generator-mastery-create-iam-sc300-practice-pbqs
  Complete SC-300 and CyberArk Defender PBQ generation guide

## How They Work Together

| Tool | Format | Best For |
|------|--------|----------|
| GIDEON Log Analysis (free) | Open-ended scenarios | Building analysis skills |
| Udemy Practice Tests (paid) | Multiple choice with explanations | Testing and reinforcing knowledge |

Use GIDEON to build the skill. Use the Udemy course to test the knowledge.

## About

Built by John Pickering as a free companion tool for cybersecurity certification students.

Star this repo if you find it useful!
