"""
GIDEON CySA+ CS0-004 (V4) Module
=================================
Drop this file into your GIDEON project folder.
Add "CySA+ CS0-004" as an exam option in your main menu
and call generate_cysa_pbq() from your existing generator logic.

Domains and weights:
  1. Security Operations         34%
  2. Vulnerability Management    26%
  3. Incident Response           24%
  4. Reporting & Communication   16%
"""

import random

# ─────────────────────────────────────────────
#  EXAM METADATA
# ─────────────────────────────────────────────

CYSA_EXAM = {
    "code": "CS0-004",
    "name": "CompTIA CySA+",
    "version": "V4",
    "domains": {
        "1": {"name": "Security Operations",          "weight": 34},
        "2": {"name": "Vulnerability Management",     "weight": 26},
        "3": {"name": "Incident Response & Management","weight": 24},
        "4": {"name": "Reporting & Communication",    "weight": 16},
    }
}

# ─────────────────────────────────────────────
#  DOMAIN 1 — SECURITY OPERATIONS (34%)
#  Sub-topics: logging, architecture, detection,
#  tools, threat intel/hunting, AI in SecOps
# ─────────────────────────────────────────────

DOMAIN1_SCENARIOS = [

    # --- SIEM / LOG ANALYSIS ---
    {
        "id": "D1-001",
        "domain": "1",
        "sub_topic": "SIEM Log Analysis",
        "objective": "1.3 - Indicators of malicious activity",
        "scenario_template": """
You are a Tier 2 SOC analyst. Your SIEM has generated the following alert summary
for the past 60 minutes on host WKSTN-{host_id}:

  - 47 failed login attempts from IP {src_ip} (external)
  - 1 successful login at {login_time} UTC
  - New process spawned: {suspicious_process}
  - Outbound connection to {c2_ip}:{c2_port} established 4 minutes after login
  - 2.3 GB data transferred outbound over the next 30 minutes

Questions:
1. What attack technique is most likely represented by the failed logins followed
   by a single success? Map it to the MITRE ATT&CK framework.
2. The process {suspicious_process} is a Living-off-the-Land Binary (LOLBin).
   Explain why threat actors use LOLBins and how you would detect them.
3. Based on the outbound transfer volume and timing, what stage of the kill chain
   is this? What is your immediate containment action?
4. Write a SIEM correlation rule (in plain logic, not vendor-specific syntax)
   that would alert on this pattern in future.
""",
        "variables": {
            "host_id": ["114", "227", "089", "301"],
            "src_ip": ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "login_time": ["02:14", "03:47", "01:58", "04:22"],
            "suspicious_process": ["certutil.exe", "mshta.exe", "regsvr32.exe", "wscript.exe"],
            "c2_ip": ["198.51.100.22", "203.0.113.5", "192.0.2.88"],
            "c2_port": ["443", "8080", "4444", "8443"],
        },
        "exam_objectives": ["1.1", "1.2", "1.3", "1.4"],
        "difficulty": "intermediate",
    },

    # --- PACKET ANALYSIS ---
    {
        "id": "D1-002",
        "domain": "1",
        "sub_topic": "Packet Analysis",
        "objective": "1.3 - Network indicators",
        "scenario_template": """
You are analysing a pcap file captured on the perimeter firewall.
You observe the following in Wireshark:

  - Source: {internal_host}
  - Multiple SYN packets to {target_ip} on sequential ports
    ({port_start} through {port_end}) within 2 seconds
  - No SYN-ACK responses received for most ports
  - SYN-ACK received on port {open_port}
  - Followed immediately by a connection attempt on that port

Questions:
1. Identify the scanning technique being used. Is this likely automated or manual?
2. Write a Snort/Suricata rule that would detect this activity.
3. The internal host {internal_host} is a developer workstation.
   What are two plausible explanations — one benign, one malicious?
4. What additional log sources would you correlate to determine intent?
""",
        "variables": {
            "internal_host": ["10.10.5.44", "172.16.20.10", "10.0.1.88"],
            "target_ip": ["10.10.100.5", "192.168.50.1", "10.0.50.200"],
            "port_start": ["20", "79", "135"],
            "port_end": ["1024", "445", "500"],
            "open_port": ["22", "3389", "8080", "445"],
        },
        "exam_objectives": ["1.2", "1.3"],
        "difficulty": "intermediate",
    },

    # --- THREAT HUNTING ---
    {
        "id": "D1-003",
        "domain": "1",
        "sub_topic": "Threat Hunting",
        "objective": "1.4 - Threat intelligence and hunting",
        "scenario_template": """
Your threat intelligence platform (TIP) has ingested a new report indicating
that APT group {apt_group} is actively targeting organisations in your sector
using {attack_technique}.

The IoCs shared include:
  - File hash (SHA-256): {file_hash}
  - C2 domain: {c2_domain}
  - Registry key: {registry_key}

You have been asked to lead a threat hunt across your environment.

Questions:
1. Define your threat hunting hypothesis for this hunt in one sentence.
2. List the data sources you would query and the specific fields you would
   look for in each.
3. Using the Pyramid of Pain, classify each of the three IoCs above.
   Which is most valuable for long-term detection and why?
4. If the file hash is found on an endpoint, outline your next five steps
   in order, referencing the MITRE ATT&CK technique for {attack_technique}.
5. After the hunt, how do you document findings for future detection engineering?
""",
        "variables": {
            "apt_group": ["APT29", "Lazarus Group", "FIN7", "APT41"],
            "attack_technique": [
                "spear-phishing with malicious Office macros",
                "DLL side-loading via legitimate software updaters",
                "credential stuffing against VPN endpoints",
                "supply chain compromise via third-party software",
            ],
            "file_hash": [
                "3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4",
                "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
            ],
            "c2_domain": ["update-srv.net", "cdn-delivery.io", "telemetry-api.com"],
            "registry_key": [
                r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svcupdate",
                r"HKLM\SOFTWARE\Classes\CLSID\{GUID}\InprocServer32",
            ],
        },
        "exam_objectives": ["1.4"],
        "difficulty": "advanced",
    },

    # --- AI IN SECURITY OPERATIONS ---
    {
        "id": "D1-004",
        "domain": "1",
        "sub_topic": "AI in Security Operations",
        "objective": "1.5 - AI risks and use cases in SecOps",
        "scenario_template": """
Your SOC has recently deployed an AI-assisted log analysis tool.
A junior analyst runs the following query:

  "Summarise all security events for the past 7 days and identify
   any threats. Our environment includes {sensitive_system}."

The AI tool returns a detailed summary that includes:
  - Internal IP ranges
  - Names of privileged accounts
  - Details of a current IR investigation

Questions:
1. Identify TWO AI-specific risks demonstrated in this scenario.
   Use the correct terminology from the CS0-004 objectives.
2. The analyst copy-pasted raw log data (including PII) into the AI tool.
   What governance control should have prevented this?
3. Write a 5-point AI Usage Policy for SOC analysts covering:
   approved tools, sensitive data handling, output verification,
   logging of AI interactions, and escalation procedures.
4. The AI tool later flags a {false_positive_event} as a critical threat.
   How do you validate or refute this finding without over-relying on the AI?
""",
        "variables": {
            "sensitive_system": [
                "our PCI-DSS cardholder data environment",
                "our HR payroll system containing PII",
                "our OT/SCADA network",
            ],
            "false_positive_event": [
                "scheduled backup job as ransomware",
                "vulnerability scanner as an active attack",
                "legitimate admin PowerShell script as malware",
            ],
        },
        "exam_objectives": ["1.5"],
        "difficulty": "intermediate",
    },

    # --- IDENTITY / IAM INDICATORS ---
    {
        "id": "D1-005",
        "domain": "1",
        "sub_topic": "Identity-Based Indicators",
        "objective": "1.3 - Identity indicators, impossible travel, BEC",
        "scenario_template": """
Your Microsoft Entra ID (Azure AD) monitoring has generated the following alerts
for user account {user_account}:

  08:15 UTC  — Successful login from Auckland, New Zealand (usual location)
  08:47 UTC  — Successful login from {foreign_city} (new location, never seen before)
  08:48 UTC  — New mail forwarding rule created: all email → {external_email}
  09:02 UTC  — {num_emails} emails sent to external vendors with subject
               "Updated payment details — action required"
  09:10 UTC  — Access to SharePoint HR salary data

Questions:
1. What is the name of the indicator shown between the 08:15 and 08:47 logins?
   What does it tell you about the attack?
2. The mail forwarding rule and vendor emails indicate what type of attack?
   What financial risk does this represent?
3. List your immediate containment steps in order (at least 5 steps).
4. Which Microsoft 365 / Entra ID logs would you preserve as forensic evidence
   and why?
5. This account did not have MFA enabled. What Conditional Access policy would
   have most likely prevented this compromise?
""",
        "variables": {
            "user_account": ["j.smith@contoso.com", "a.jones@fabrikam.com", "cfo@tailwind.com"],
            "foreign_city": ["Bucharest, Romania", "Lagos, Nigeria", "Moscow, Russia"],
            "external_email": ["payments@gmail.com", "finance-dept@protonmail.com"],
            "num_emails": ["12", "28", "7"],
        },
        "exam_objectives": ["1.3"],
        "difficulty": "intermediate",
    },
]

# ─────────────────────────────────────────────
#  DOMAIN 2 — VULNERABILITY MANAGEMENT (26%)
#  Sub-topics: scanning, analysis, prioritisation,
#  treatment, validation, patch management
# ─────────────────────────────────────────────

DOMAIN2_SCENARIOS = [

    # --- VULNERABILITY SCAN ANALYSIS ---
    {
        "id": "D2-001",
        "domain": "2",
        "sub_topic": "Vulnerability Scan Analysis",
        "objective": "2.2 - Analyse and prioritise vulnerabilities",
        "scenario_template": """
You have just completed a credentialed internal vulnerability scan of your
{environment_type} environment using {scanner_tool}.

The scan returned the following findings:

  CVE              | CVSS Score | Asset                  | Exploitability
  -----------------|------------|------------------------|----------------
  CVE-{cve1}      |    {cvss1} | Domain Controller DC01 | Public exploit available
  CVE-{cve2}      |    {cvss2} | Web server DMZ-WEB01   | PoC only
  CVE-{cve3}      |    {cvss3} | Dev workstation DEV-04  | No known exploit
  CVE-{cve4}      |    {cvss4} | Printer PRINT-02        | No known exploit

Questions:
1. Rank these vulnerabilities for remediation priority. Do NOT use CVSS score alone —
   explain each factor you consider (asset criticality, exploitability, exposure).
2. CVE-{cve1} affects your Domain Controller. Patching requires a reboot and a
   30-minute maintenance window. Your change freeze ends in 14 days.
   What compensating control would you implement immediately?
3. The web server CVE-{cve2} is in the DMZ and internet-facing.
   How does this change your prioritisation compared to the same CVE
   on an internal-only server?
4. DEV-04 is a developer laptop not covered by your patch management tool.
   How do you handle vulnerability management for unmanaged endpoints?
5. Write a one-paragraph executive summary of the scan results suitable
   for your CISO.
""",
        "variables": {
            "environment_type": ["on-premises Windows Server", "hybrid cloud (Azure + on-prem)", "AWS cloud-only"],
            "scanner_tool": ["Nessus", "Qualys", "Rapid7 InsightVM", "OpenVAS"],
            "cve1": ["2024-21413", "2023-44487", "2024-30078"],
            "cve2": ["2024-21338", "2023-38545", "2024-20353"],
            "cve3": ["2023-36884", "2024-26198", "2023-23397"],
            "cve4": ["2022-30190", "2023-21554", "2024-21447"],
            "cvss1": ["9.8", "9.6", "9.4"],
            "cvss2": ["8.1", "7.8", "8.8"],
            "cvss3": ["6.5", "5.9", "6.1"],
            "cvss4": ["4.3", "3.7", "4.8"],
        },
        "exam_objectives": ["2.1", "2.2"],
        "difficulty": "intermediate",
    },

    # --- CLOUD VULNERABILITY ASSESSMENT ---
    {
        "id": "D2-002",
        "domain": "2",
        "sub_topic": "Cloud Vulnerability Assessment",
        "objective": "2.1 - Scanning approaches including cloud",
        "scenario_template": """
Your organisation has {num_buckets} Amazon S3 buckets and {num_ec2} EC2 instances.
A cloud security posture scan using {cloud_tool} has returned these findings:

  CRITICAL: S3 bucket "{bucket_name}" is publicly readable — contains {data_type}
  HIGH:     EC2 instance i-{instance_id} is running {old_os} (end of support {eos_date})
  HIGH:     Security group sg-{sg_id} allows inbound {risky_port}/TCP from 0.0.0.0/0
  MEDIUM:   {num_keys} IAM access keys have not been rotated in over 90 days
  MEDIUM:   CloudTrail logging disabled in {aws_region} region

Questions:
1. The S3 bucket exposure is CRITICAL. Walk through your immediate response
   steps — what do you do in the first 15 minutes?
2. Explain the difference between agent-based and agentless scanning in a
   cloud environment. Which did {cloud_tool} most likely use for the EC2 finding?
3. The security group allows {risky_port}/TCP from 0.0.0.0/0. What service
   typically uses this port and why is this dangerous even if the service
   is patched?
4. CloudTrail is disabled in {aws_region}. What is the forensic impact of this
   if the S3 breach occurred in that region?
5. Create a remediation action plan with owners, timelines, and success criteria
   for all five findings.
""",
        "variables": {
            "num_buckets": ["14", "32", "7"],
            "num_ec2": ["28", "55", "12"],
            "cloud_tool": ["ScoutSuite", "Prowler", "AWS Security Hub", "Trivy"],
            "bucket_name": ["hr-payroll-exports", "customer-pii-backup", "finance-reports-2024"],
            "data_type": ["employee PII and salary data", "customer credit card records", "health records"],
            "instance_id": ["0abc1234def", "1bcd5678ef0", "2cde9012fab"],
            "old_os": ["Windows Server 2012 R2", "Ubuntu 18.04 LTS", "CentOS 7"],
            "eos_date": ["October 2023", "April 2023", "June 2024"],
            "sg_id": ["0a1b2c3d", "4e5f6a7b", "8c9d0e1f"],
            "risky_port": ["3389", "22", "23", "5900"],
            "num_keys": ["8", "15", "23"],
            "aws_region": ["ap-southeast-2", "us-east-1", "eu-west-1"],
        },
        "exam_objectives": ["2.1", "2.2"],
        "difficulty": "advanced",
    },

    # --- PATCH MANAGEMENT & REMEDIATION ---
    {
        "id": "D2-003",
        "domain": "2",
        "sub_topic": "Patch Management and Remediation Validation",
        "objective": "2.3 - Vulnerability treatment and validation",
        "scenario_template": """
You manage vulnerability remediation for a {org_size} organisation.
This month's patch cycle must address:

  - {num_critical} CRITICAL patches (including one for {critical_vuln})
  - {num_high} HIGH patches across {num_systems} systems
  - {num_medium} MEDIUM patches (mostly third-party software)

Your constraints:
  - Change freeze: none currently
  - Maintenance windows: Saturdays 02:00–06:00 NZST only
  - {num_systems} systems across {num_sites} sites
  - {legacy_system} cannot be patched — vendor no longer supports it

Questions:
1. Define your patching SLA targets for CRITICAL, HIGH, and MEDIUM findings.
   Justify each timeline.
2. {critical_vuln} is being actively exploited in the wild (CISA KEV listed).
   You cannot patch within 24 hours due to testing requirements.
   What compensating controls do you implement?
3. {legacy_system} cannot receive patches. Document your risk acceptance process —
   what must be included and who must sign off?
4. After patching, how do you validate remediation was successful?
   List at least three validation methods.
5. Three systems failed to patch due to agent connectivity issues.
   How do you track and manage these exceptions?
""",
        "variables": {
            "org_size": ["200-person", "500-person", "50-person"],
            "num_critical": ["3", "7", "12"],
            "critical_vuln": [
                "MS Exchange Remote Code Execution (ProxyShell-style)",
                "Cisco IOS XE privilege escalation",
                "VMware vCenter unauthenticated RCE",
            ],
            "num_high": ["18", "34", "9"],
            "num_systems": ["120", "280", "45"],
            "num_medium": ["47", "92", "21"],
            "num_sites": ["3", "6", "1"],
            "legacy_system": [
                "a Windows Server 2008 R2 production database server",
                "a CNC manufacturing control system running XP",
                "a medical imaging device running Windows 7",
            ],
        },
        "exam_objectives": ["2.2", "2.3"],
        "difficulty": "intermediate",
    },
]

# ─────────────────────────────────────────────
#  DOMAIN 3 — INCIDENT RESPONSE (24%)
#  Sub-topics: IR lifecycle, frameworks,
#  containment, forensics, eradication,
#  recovery, post-incident
# ─────────────────────────────────────────────

DOMAIN3_SCENARIOS = [

    # --- RANSOMWARE IR ---
    {
        "id": "D3-001",
        "domain": "3",
        "sub_topic": "Ransomware Incident Response",
        "objective": "3.2 - IR lifecycle: detect, contain, eradicate, recover",
        "scenario_template": """
It is {time_of_day} on a {day_of_week}. You receive a call — users across
{num_sites} sites cannot access files. File shares show files renamed with
extension ".{ransom_ext}". A ransom note "{ransom_note_file}" has appeared
on every desktop.

Initial investigation shows:
  - Patient zero: workstation {patient_zero} (user: {compromised_user})
  - Attack vector appears to be {attack_vector}
  - {num_encrypted} systems show encrypted files so far
  - Backups are stored on {backup_location}
  - Your RTO is {rto} hours

Questions:
1. You have 5 minutes to make your first decision. Do you isolate immediately
   or observe longer? Justify using the IR lifecycle framework.
2. Map this incident to the Cyber Kill Chain. At which stage was detection?
   What stages had already completed?
3. {backup_location} — are your backups safe? What is your first action
   regarding backups?
4. Write your incident declaration message (3–4 sentences) to send to
   senior management right now.
5. After containment, outline your eradication steps before you begin recovery.
   What must you confirm before restoring from backup?
6. Your RTO is {rto} hours. You are currently at hour 2.
   Build a recovery priority list — which systems do you restore first and why?
""",
        "variables": {
            "time_of_day": ["02:30", "Friday 17:45", "Monday 08:15", "Saturday 11:20"],
            "day_of_week": ["Tuesday", "Friday", "Monday", "Saturday"],
            "num_sites": ["2", "4", "1"],
            "ransom_ext": ["encrypted", "locked", "WASTED", "crypt"],
            "ransom_note_file": ["READ_ME_NOW.txt", "YOUR_FILES_ARE_GONE.html", "DECRYPT_INFO.txt"],
            "patient_zero": ["WKSTN-047", "LAPTOP-CEO-01", "RECEPTION-PC"],
            "compromised_user": ["j.wilson (Finance)", "reception@company.com", "m.patel (HR)"],
            "attack_vector": [
                "a malicious Excel macro attachment opened from a phishing email",
                "RDP brute force from an exposed RDP port",
                "a compromised MSP remote management agent",
            ],
            "num_encrypted": ["14", "67", "3", "130"],
            "backup_location": [
                "a NAS device on the same network segment (currently accessible)",
                "Azure Blob Storage with immutable backup policies enabled",
                "tape backups stored off-site (last backup: 3 days ago)",
            ],
            "rto": ["4", "8", "24", "48"],
        },
        "exam_objectives": ["3.1", "3.2", "3.3"],
        "difficulty": "advanced",
    },

    # --- FORENSIC EVIDENCE & CHAIN OF CUSTODY ---
    {
        "id": "D3-002",
        "domain": "3",
        "sub_topic": "Digital Forensics and Evidence Handling",
        "objective": "3.2 - Forensic analysis and evidence preservation",
        "scenario_template": """
A disgruntled employee, {employee_name} ({role}), is suspected of
{suspected_activity} before resigning last {resign_day}.

HR has asked you to conduct a forensic investigation.
The employee used: {device_type} (asset tag: {asset_tag}).

Questions:
1. Before touching the device, what is the FIRST thing you must ensure is in place?
   Why is this critical to any potential legal proceeding?
2. Describe your evidence collection process for {device_type}.
   Include: order of volatility, imaging method, and hash verification.
3. List FIVE specific artefacts you would examine on this device and explain
   what each might reveal about {suspected_activity}.
4. The employee also had access to Microsoft 365 and OneDrive.
   What cloud-based evidence sources would you request and from whom?
5. Write a Chain of Custody entry for the initial seizure of {device_type}.
   Include all required fields.
6. HR wants the results by tomorrow morning. What do you tell them about
   realistic forensic timelines and why rushing could be harmful?
""",
        "variables": {
            "employee_name": ["R. Thompson", "S. Nakamura", "D. O'Brien"],
            "role": ["Senior Developer", "Finance Analyst", "Sales Manager"],
            "suspected_activity": [
                "exfiltrating customer database records to a personal USB drive",
                "deleting critical project files before departure",
                "copying proprietary source code to personal cloud storage",
            ],
            "resign_day": ["Friday", "Wednesday", "Monday"],
            "device_type": ["company-issued Windows 11 laptop", "company iPhone 15", "shared workstation"],
            "asset_tag": ["IT-2847", "MOB-0391", "SHR-0102"],
        },
        "exam_objectives": ["3.2"],
        "difficulty": "advanced",
    },

    # --- TABLETOP EXERCISE ---
    {
        "id": "D3-003",
        "domain": "3",
        "sub_topic": "IR Readiness and Tabletop Exercise",
        "objective": "3.1 - IR planning, playbooks, tabletop exercises",
        "scenario_template": """
You are facilitating a tabletop exercise for your organisation.

Scenario inject: Your {cloud_provider} environment has been breached.
The attacker used {initial_access} to gain access {days_ago} days ago.
They have maintained persistence using {persistence_technique} and have
had read access to {sensitive_data} for approximately {days_ago} days.

You have just discovered this through {detection_method}.

Discussion questions for the tabletop:
1. What should your IR plan have included to detect this {days_ago} days earlier?
   Identify at least two specific detection controls that were missing.
2. Who needs to be notified, in what order, and within what timeframes?
   Include internal stakeholders AND any legal/regulatory notification requirements.
3. Your {cloud_provider} environment has {cloud_complexity} — how does this
   affect your containment strategy compared to a pure on-premises environment?
4. The attacker has had access for {days_ago} days. How does this affect your
   scope of investigation and your breach notification obligations?
5. After the exercise, what THREE improvements would you prioritise in your
   IR plan and why?
""",
        "variables": {
            "cloud_provider": ["Microsoft Azure", "AWS", "Google Cloud"],
            "initial_access": [
                "a compromised service account with no MFA",
                "a publicly exposed storage container with weak credentials",
                "a phishing email that captured an admin's credentials",
            ],
            "days_ago": ["14", "30", "7", "45"],
            "persistence_technique": [
                "a backdoor OAuth application with delegated permissions",
                "a new privileged IAM user created in a secondary region",
                "a scheduled task on a compromised EC2 instance",
            ],
            "sensitive_data": [
                "customer PII including names, emails, and addresses",
                "intellectual property — product source code",
                "financial records including bank account details",
            ],
            "detection_method": [
                "an anonymous tip from a dark web monitoring service",
                "an anomaly alert from your UEBA tool",
                "a customer complaint about suspicious activity",
            ],
            "cloud_complexity": [
                "resources spread across 4 regions and 3 subscriptions",
                "a microservices architecture with 200+ services",
                "shared responsibility boundaries with a SaaS provider",
            ],
        },
        "exam_objectives": ["3.1", "3.3"],
        "difficulty": "intermediate",
    },
]

# ─────────────────────────────────────────────
#  DOMAIN 4 — REPORTING & COMMUNICATION (16%)
#  Sub-topics: vulnerability reports, IR reports,
#  metrics, stakeholder comms, RCA
# ─────────────────────────────────────────────

DOMAIN4_SCENARIOS = [

    # --- EXECUTIVE REPORTING ---
    {
        "id": "D4-001",
        "domain": "4",
        "sub_topic": "Vulnerability Reporting and Metrics",
        "objective": "4.1 - Vulnerability reporting and communication",
        "scenario_template": """
End of quarter. You must present vulnerability management metrics to the board.
Your data for Q{quarter}:

  - Total vulnerabilities discovered: {total_vulns}
  - Critical (patched within SLA): {critical_patched}% ({critical_total} total)
  - High (patched within SLA): {high_patched}% ({high_total} total)
  - Mean Time to Remediate (MTTR) Critical: {mttr_days} days
  - Repeat findings (same vuln, same asset, multiple quarters): {repeat_pct}%
  - Scan coverage: {scan_coverage}% of total asset inventory

The board has {board_tech_level} technical knowledge.

Questions:
1. Rewrite the raw metrics above into a board-appropriate narrative (4–5 sentences).
   No technical jargon. Focus on business risk and trend.
2. Your MTTR for critical vulns is {mttr_days} days. Industry benchmark is 15 days.
   How do you present this and what is your improvement plan?
3. {repeat_pct}% repeat findings is a significant problem. What does this indicate
   about your remediation process and how do you address it?
4. Design THREE KPIs you would track going forward to demonstrate programme maturity.
   For each: metric name, how measured, target value, reporting frequency.
5. A board member asks: "Are we compliant?" — how do you answer this accurately
   without overcommitting?
""",
        "variables": {
            "quarter": ["1", "2", "3", "4"],
            "total_vulns": ["847", "1,203", "412", "2,891"],
            "critical_patched": ["67", "45", "82", "91"],
            "critical_total": ["24", "38", "11", "56"],
            "high_patched": ["71", "58", "88", "79"],
            "high_total": ["143", "287", "67", "412"],
            "mttr_days": ["23", "41", "12", "67"],
            "repeat_pct": ["18", "32", "8", "44"],
            "scan_coverage": ["78", "91", "64", "55"],
            "board_tech_level": ["limited", "moderate", "mixed"],
        },
        "exam_objectives": ["4.1"],
        "difficulty": "intermediate",
    },

    # --- POST-INCIDENT REPORT & RCA ---
    {
        "id": "D4-002",
        "domain": "4",
        "sub_topic": "Post-Incident Report and Root Cause Analysis",
        "objective": "4.2 - IR reporting, RCA, lessons learned",
        "scenario_template": """
You have just resolved a {incident_type} incident that:
  - Lasted {duration_hours} hours from detection to resolution
  - Affected {num_users} users and {num_systems} systems
  - Resulted in {business_impact}
  - Was caused initially by {root_cause}
  - Was detected by {detection_method}
  - Involved a regulatory notification requirement under {regulation}

Questions:
1. Write the executive summary section of your Post-Incident Report (PIR)
   in 150 words or fewer. Include: what happened, impact, and resolution.
2. Conduct a 5-Why Root Cause Analysis starting from "{root_cause}".
   Present all 5 levels clearly.
3. Your detection time was {detection_delay} hours after the initial compromise.
   Identify TWO specific lessons learned that would reduce detection time.
4. Under {regulation}, what are your notification obligations?
   What information must be included and what is the deadline?
5. List FIVE concrete recommendations from this incident with:
   - The recommendation
   - The control it addresses
   - The owner responsible
   - The target completion date (relative, e.g., "30 days")
""",
        "variables": {
            "incident_type": [
                "Business Email Compromise (BEC)",
                "ransomware",
                "data breach involving customer PII",
                "insider threat data exfiltration",
            ],
            "duration_hours": ["6", "18", "72", "4"],
            "num_users": ["1", "47", "200+", "3"],
            "num_systems": ["1", "14", "all file servers", "3"],
            "business_impact": [
                "$47,000 fraudulent wire transfer",
                "48-hour operational outage",
                "exposure of 12,000 customer records",
                "loss of proprietary source code",
            ],
            "root_cause": [
                "an account with no MFA enabled was phished",
                "an unpatched internet-facing vulnerability was exploited",
                "a misconfigured S3 bucket was publicly accessible",
                "a terminated employee's account was not disabled",
            ],
            "detection_method": [
                "a customer complaint",
                "automated SIEM alert",
                "dark web monitoring service",
                "internal user report",
            ],
            "regulation": ["GDPR", "NZ Privacy Act 2020", "HIPAA", "PCI DSS"],
            "detection_delay": ["4", "12", "72", "1"],
        },
        "exam_objectives": ["4.2"],
        "difficulty": "advanced",
    },
]

# ─────────────────────────────────────────────
#  ALL SCENARIOS — COMBINED POOL
# ─────────────────────────────────────────────

ALL_CYSA_SCENARIOS = (
    DOMAIN1_SCENARIOS +
    DOMAIN2_SCENARIOS +
    DOMAIN3_SCENARIOS +
    DOMAIN4_SCENARIOS
)

# ─────────────────────────────────────────────
#  CORE GENERATOR FUNCTION
# ─────────────────────────────────────────────

def generate_cysa_pbq(domain_filter=None, difficulty_filter=None):
    """
    Generate one CySA+ CS0-004 PBQ scenario with randomised variables.

    Args:
        domain_filter   : "1", "2", "3", or "4" — or None for any domain
        difficulty_filter: "beginner", "intermediate", or "advanced" — or None

    Returns:
        dict with keys: id, domain_name, objective, difficulty, scenario (str)
    """
    pool = ALL_CYSA_SCENARIOS

    if domain_filter:
        pool = [s for s in pool if s["domain"] == str(domain_filter)]

    if difficulty_filter:
        filtered = [s for s in pool if s["difficulty"] == difficulty_filter]
        if filtered:
            pool = filtered
        # else fall back to full domain pool

    template = random.choice(pool)
    scenario_text = template["scenario_template"]

    # Substitute all variables with random choices
    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace(f"{{{var_name}}}", chosen)

    domain_info = CYSA_EXAM["domains"][template["domain"]]

    return {
        "exam":        f"{CYSA_EXAM['name']} {CYSA_EXAM['code']} ({CYSA_EXAM['version']})",
        "id":          template["id"],
        "domain":      f"{template['domain']}. {domain_info['name']} ({domain_info['weight']}%)",
        "sub_topic":   template["sub_topic"],
        "objective":   template["objective"],
        "difficulty":  template["difficulty"],
        "exam_objectives": ", ".join(template.get("exam_objectives", [])),
        "scenario":    scenario_text.strip(),
    }


def get_weighted_cysa_pbq():
    """
    Generate a PBQ respecting the official CS0-004 domain weighting:
      Domain 1 (Security Operations)       — 34%
      Domain 2 (Vulnerability Management)  — 26%
      Domain 3 (Incident Response)         — 24%
      Domain 4 (Reporting & Communication) — 16%
    """
    weights = [34, 26, 24, 16]
    domain = random.choices(["1", "2", "3", "4"], weights=weights, k=1)[0]
    return generate_cysa_pbq(domain_filter=domain)


def display_pbq(pbq: dict):
    """Pretty-print a PBQ to the terminal — matches GIDEON's existing output style."""
    separator = "=" * 70
    print(f"\n{separator}")
    print(f"  {pbq.get('exam', 'CySA+ CS0-004')}")
    print(f"  Scenario ID : {pbq.get('id', 'N/A')}")
    print(f"  Domain      : {pbq.get('domain', 'N/A')}")
    print(f"  Sub-topic   : {pbq.get('sub_topic', 'N/A')}")
    print(f"  Objective   : {pbq.get('objective', 'N/A')}")
    print(f"  Difficulty  : {pbq.get('difficulty', 'N/A').upper()}")
    print(f"  Obj. Refs   : {pbq.get('exam_objectives', 'N/A')}")
    print(separator)
    print(pbq.get("scenario", "No scenario generated."))
    print(f"\n{separator}\n")


# ─────────────────────────────────────────────
#  QUICK TEST — run this file directly to verify
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\nGIDEON — CySA+ CS0-004 Module Test")
    print("Generating 3 sample PBQs (weighted by domain)...\n")

    for i in range(3):
        pbq = get_weighted_cysa_pbq()
        display_pbq(pbq)
        input("Press ENTER for next scenario...\n")