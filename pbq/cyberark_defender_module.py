"""
GIDEON CyberArk Defender PAM-DEF Module
========================================
CyberArk Defender - PAM (PAM-DEF)
7 Knowledge Domains (Official CyberArk Study Guide):
  1. Account Onboarding
  2. Application Management
  3. Ongoing Maintenance
  4. Password Management Configuration
  5. Security and Audit
  6. Session Management Configuration
  7. User Management Configuration
"""

import random

CYBERARK_EXAM = {
    "code": "PAM-DEF",
    "name": "CyberArk Defender - PAM",
    "version": "2025",
    "domains": {
        "1": {"name": "Account Onboarding",                "weight": "15"},
        "2": {"name": "Application Management",            "weight": "10"},
        "3": {"name": "Ongoing Maintenance",               "weight": "15"},
        "4": {"name": "Password Management Configuration", "weight": "15"},
        "5": {"name": "Security and Audit",                "weight": "15"},
        "6": {"name": "Session Management Configuration",  "weight": "20"},
        "7": {"name": "User Management Configuration",     "weight": "10"},
    }
}

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 1 ??" ACCOUNT ONBOARDING
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN1_SCENARIOS = [
    {
        "id": "CA1-001",
        "domain": "1",
        "sub_topic": "Account Discovery and Onboarding",
        "objective": "1.1 - Onboard accounts using Account Discovery and Password Upload Utility",
        "scenario_template": """
You are a CyberArk administrator at {org_name}, a {org_size} organisation.
The security team has identified {num_accounts} unmanaged privileged accounts
across {num_servers} Windows servers that need to be onboarded to the Vault.

Current state:
  - Accounts include: local Administrator accounts, service accounts, and
    {special_account_type} accounts
  - Servers are spread across {num_domains} Active Directory domains
  - Some accounts have unknown passwords
  - The team wants to use the most efficient onboarding method

Questions:
1. Compare the three main methods for onboarding accounts in CyberArk:
   Manual (PVWA), Password Upload Utility (PUU), and Account Discovery.
   Which would you recommend for {num_accounts} accounts and why?
2. When using Account Discovery, what is the difference between an
   Active Directory scan and a network scan? Which is more appropriate
   for domain-joined Windows accounts?
3. {num_accounts} accounts need to be assigned to Safes. Design a Safe
   structure for these accounts considering least privilege and separation
   of duties. How many Safes would you create and what naming convention
   would you use?
4. Some accounts have unknown passwords. Walk through the process of
   onboarding an account with an unknown password in CyberArk.
   What happens after onboarding?
5. After onboarding, the CPM fails to verify {num_failed} accounts.
   List the most common reasons for CPM verification failure and how
   you would troubleshoot each one.
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Ltd", "Northwind Industries", "Alpine Systems"],
            "org_size": ["500-person", "2,000-person", "800-person", "5,000-person"],
            "num_accounts": ["450", "1,200", "280", "750"],
            "num_servers": ["120", "400", "90", "250"],
            "special_account_type": ["SQL Server service", "IIS application pool", "scheduled task", "backup agent"],
            "num_domains": ["2", "4", "1", "3"],
            "num_failed": ["12", "35", "8", "22"],
        },
        "exam_objectives": ["1.1", "1.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA1-001: Account Discovery and Onboarding

Q1 ??" Onboarding method comparison
Manual (PVWA): Add account one at a time via the Accounts page. Suitable
for small numbers (under 20). Not scalable.
Password Upload Utility (PUU): CSV-based bulk import tool. Runs from command
line. Best for large batches of known accounts with known passwords.
Account Discovery: Automated scan of AD or network to find unmanaged accounts.
Best for discovering unknown accounts before onboarding.
Recommendation: For 450-1,200 accounts, use Account Discovery first to find
all accounts, then PUU to bulk onboard them to the Vault.

Q2 ??" AD scan vs network scan
AD scan: queries Active Directory to find computer objects and then scans
those computers for local accounts. More accurate for domain-joined machines,
uses AD authentication, respects OU structure.
Network scan: scans IP ranges to find machines regardless of AD membership.
Better for non-domain machines (Linux, network devices).
For domain-joined Windows accounts: use Active Directory scan ??" it is more
accurate and integrates with existing AD structure.

Q3 ??" Safe structure design
Best practice: separate Safes by function and team, not by server.
Recommended structure:
  - Windows-LocalAdmin-[Region/Team] ??" for local Administrator accounts
  - ServiceAccounts-[Application/Team] ??" for service accounts by app owner
  - DBAccounts-[DatabaseTeam] ??" for SQL/database accounts
  - EmergencyAccess ??" for break-glass accounts (highly restricted)
Naming convention: [AccountType]-[Team/Function]-[Environment]
Typical result: 4-8 Safes for this environment.
Each Safe should have a defined Owner, CPM, and access group.

Q4 ??" Onboarding account with unknown password
In PVWA: Add Account ??' fill in account details ??' select "The password is
unknown" checkbox. CyberArk stores the account with a temporary placeholder.
After onboarding: the CPM immediately attempts to change the password to a
new random password that meets the platform policy. The new password is
stored in the Vault and the account is now managed.
Important: ensure the CPM has sufficient permissions on the target system
to change the password before selecting this option.

Q5 ??" CPM verification failure causes and troubleshooting
Common causes:
  1. Account locked out ??' check AD account status, unlock if needed
  2. Password changed manually outside CyberArk ??' trigger CPM reconcile
  3. CPM network connectivity issue ??' check firewall rules between CPM and target
  4. Wrong platform assigned ??' verify platform matches the account type (Windows/Unix)
  5. Insufficient CPM permissions on target ??' verify CPM service account has
     the right local admin or domain permissions
  6. Target machine offline/unreachable ??' verify machine is online
Troubleshooting path: PVWA ??' Accounts ??' [account] ??' CPM Status ??' view
error message ??' check CPMLog on the CPM server for detailed error.
"""
    },
    {
        "id": "CA1-002",
        "domain": "1",
        "sub_topic": "Platform Assignment and Safe Structure",
        "objective": "1.2 - Assign accounts to appropriate platforms and Safes",
        "scenario_template": """
You are onboarding privileged accounts for {org_name}. The environment includes:

  - {num_windows} Windows local Administrator accounts (domain-joined)
  - {num_unix} Unix root accounts on RHEL servers
  - {num_network} network device accounts (Cisco routers and switches)
  - {num_db} Oracle database SYS accounts
  - {num_cloud} AWS IAM access keys

Questions:
1. For each account type above, identify the appropriate out-of-the-box
   CyberArk platform. What is a platform and what does it define?
2. The {num_unix} Unix root accounts will use SSH key management instead
   of password management. How does CyberArk manage SSH keys and what
   platform would you use?
3. You need to create a custom platform for the {num_network} Cisco devices
   because the out-of-the-box platform doesn't support your enable password
   requirements. Walk through the process of duplicating and modifying an
   existing platform.
4. A Safe called "WinAdmins-Prod" has been created. Walk through adding the
   correct CyberArk groups to the Safe with appropriate permissions for:
   - The team who needs to use these passwords
   - The CPM that manages the passwords
   - The auditors who need read-only access
5. What is the difference between Safe-level permissions and account-level
   permissions in CyberArk? Give an example of when you would use each.
""",
        "variables": {
            "org_name": ["Contoso", "Fabrikam", "Northwind", "Alpine Corp"],
            "num_windows": ["200", "500", "150", "800"],
            "num_unix": ["80", "200", "45", "320"],
            "num_network": ["40", "100", "25", "150"],
            "num_db": ["20", "60", "12", "85"],
            "num_cloud": ["15", "50", "8", "120"],
        },
        "exam_objectives": ["1.2", "1.3"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA1-002: Platform Assignment and Safe Structure

Q1 ??" Platform identification
A Platform defines: password complexity rules, change/verify/reconcile
frequency, connection method, plugin to use, and password age policies.
Account type ??' Platform:
  - Windows local Administrator ??' WinServerLocal (or WinDesktopLocal)
  - Unix root ??' UnixSSH or UnixTelnet
  - Cisco routers/switches ??' Cisco (or CiscoEnablePassword)
  - Oracle SYS ??' Oracle (uses TNS connection)
  - AWS IAM access keys ??' AWSAccessKeys (or custom AWS platform)

Q2 ??" SSH key management in CyberArk
CyberArk can manage SSH keys in addition to passwords.
Platform: UnixSSHKeys (specific SSH key management platform).
Process: CyberArk generates a new SSH key pair, stores the private key in
the Vault, and uploads the public key to the target server's
~/.ssh/authorized_keys file.
The CPM rotates the SSH key pair on schedule ??" generating a new pair,
updating authorized_keys on the server, and storing the new private key
in the Vault. The old key is removed.

Q3 ??" Creating a custom platform
PVWA ??' Administration ??' Platform Management ??' find the closest existing
platform (e.g. Cisco) ??' Duplicate Platform ??' give it a new name.
Edit the duplicated platform:
  - Connection components: configure the enable password prompt handling
  - Password settings: set complexity, rotation frequency
  - Automatic Password Management: configure verify/change/reconcile commands
  - Test with a single account before rolling out to all network devices.
Never modify the out-of-the-box platforms directly ??" always duplicate first.

Q4 ??" Safe permissions for WinAdmins-Prod
Groups and permissions to add:
  - [Team group] e.g. WinAdmins-Users:
    List accounts, View Safe members, Use accounts, Retrieve accounts
  - [CPM group] e.g. PasswordManager (CPM service account group):
    List accounts, View Safe members, Retrieve accounts, Add accounts,
    Update account content, Update account properties, Rename accounts,
    Delete accounts, Unlock accounts
  - [Audit group] e.g. Auditors:
    List accounts, View Safe members, View audit log
Do NOT give auditors Retrieve accounts ??" they should not see passwords.

Q5 ??" Safe-level vs account-level permissions
Safe-level permissions: apply to all accounts within the Safe. Managed
via Safe Members in PVWA. This is the primary permission model.
Account-level permissions: override Safe-level permissions for a specific
account only. Used when one account in a Safe needs different access than
the rest (e.g. a highly sensitive account that only the CISO can retrieve).
Example: Auditors have View access at Safe level for all accounts, but the
CEO's personal admin account has account-level restrictions blocking even
auditors from viewing it.
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 2 ??" APPLICATION MANAGEMENT
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN2_SCENARIOS = [
    {
        "id": "CA2-001",
        "domain": "2",
        "sub_topic": "Application Identity Management (AIM/AAM)",
        "objective": "2.1 - Configure Application Identity Manager for application credentials",
        "scenario_template": """
{org_name} has {num_apps} applications that currently store database credentials
in configuration files or hardcoded in application code. The security team
wants to eliminate hardcoded credentials using CyberArk's Application
Identity Manager (AIM/AAM).

Applications include:
  - {app1}: Java web application connecting to Oracle DB
  - {app2}: .NET application connecting to SQL Server
  - {app3}: Python script running as a scheduled task
  - {app4}: Legacy application that cannot be modified (read-only binary)

Questions:
1. Explain the three methods CyberArk AIM/AAM provides for applications to
   retrieve credentials. What is the difference between the Credential Provider
   (CP), Central Credential Provider (CCP), and the SDK?
2. For {app1} (Java/Oracle), configure the CCP REST API method.
   What information does the application need to provide in the API call?
   What does CyberArk return?
3. {app4} cannot be modified at all. How can CyberArk still manage its
   credentials? What CyberArk component handles this use case?
4. Application authentication in AIM uses application identity. List the
   methods CyberArk uses to authenticate the calling application and explain
   why this matters for security.
5. Walk through creating an Application object in PVWA and granting it
   access to retrieve a specific account from a Safe. What are the
   minimum Safe permissions the Application object needs?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Ltd", "Northwind Tech", "Pacific Systems"],
            "num_apps": ["15", "32", "8", "45"],
            "app1": ["CustomerPortal", "SalesWebApp", "HRPortal", "InventorySystem"],
            "app2": ["FinanceReporter", "PayrollSystem", "BillingEngine", "ReportingService"],
            "app3": ["NightlyDataSync", "BackupValidator", "AuditCollector", "DataPurger"],
            "app4": ["LegacyERP", "OldCRMSystem", "ClassicBilling", "HeritageHRApp"],
        },
        "exam_objectives": ["2.1", "2.2"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE ??" CA2-001: Application Identity Management

Q1 ??" AIM/AAM credential retrieval methods
Credential Provider (CP): agent installed on the application server.
Application calls a local API or uses the CLIPasswordSDK. Credentials
retrieved locally ??" no network call to central server. Best for high
performance, low latency requirements.
Central Credential Provider (CCP): web service (IIS-based) that applications
call via HTTPS REST API. No agent on the app server. Best for applications
that cannot have an agent installed, or cloud/containerised apps.
SDK: programmatic integration using CyberArk's SDK libraries. More complex
but gives the most control. Embedded in application code directly.

Q2 ??" CCP REST API configuration (Java/Oracle)
Application REST API call includes:
  - AppID: the Application object name created in PVWA
  - Safe: the Safe name containing the account
  - Object (or query): the account name or search criteria
  - Authentication: certificate, IP, or OS user (configured on Application object)
CyberArk returns a JSON response containing:
  - Password (the current credential)
  - UserName
  - Address
  - Other account properties as configured
The application uses the returned password for its DB connection ??" no stored credentials.

Q3 ??" Legacy application with no code changes
Use the CyberArk Credential Provider with the CLIPasswordSDK or
the Conjur Summon tool to inject credentials at runtime via environment
variables or a wrapper script that launches the legacy application.
Alternatively: use the CyberArk On-Demand Privileges Manager (OPM) or
a secrets injection approach where a wrapper script retrieves the credential
and passes it to the legacy app as a startup parameter.
For truly unmodifiable apps: use a transparent proxy approach or
credential injection via the launch script.

Q4 ??" Application authentication methods
CyberArk authenticates the calling application using one or more of:
  1. OS User: the Windows/Unix user running the application process
  2. IP Address: the IP of the machine making the request
  3. Certificate: a client certificate presented in the HTTPS request (CCP)
  4. Machine Hash: a hash of the calling executable (CP only)
  5. Path: the filesystem path of the calling executable
Why it matters: prevents unauthorised applications from retrieving
credentials even if they know the AppID. Multiple authentication methods
can be combined (AND logic) for stronger assurance.

Q5 ??" Creating Application object and Safe permissions
PVWA ??' Applications ??' Add Application.
Fields: Application ID (unique name), Description, Business Owner,
Authentication methods (add OS user, IP, certificate as appropriate).
Safe permissions for the Application object (minimum):
  - List accounts
  - Retrieve accounts
Do NOT grant: Add, Delete, Update, or any administrative permissions.
The Application object should have the minimum permissions needed to
retrieve the specific credential ??" nothing more.
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 3 ??" ONGOING MAINTENANCE
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN3_SCENARIOS = [
    {
        "id": "CA3-001",
        "domain": "3",
        "sub_topic": "CyberArk System Health and Monitoring",
        "objective": "3.1 - Monitor CyberArk application health and perform maintenance tasks",
        "scenario_template": """
You are responsible for the ongoing maintenance of CyberArk at {org_name}.
The environment consists of:

  - {num_vaults} Digital Vaults (Primary + DR)
  - {num_cpms} CPM servers
  - {num_pvwas} PVWA servers behind a load balancer
  - {num_psms} PSM servers
  - {num_accounts} managed accounts

This morning you received alerts that {num_failed_accounts} accounts show
CPM errors and one PSM server is showing degraded performance.

Questions:
1. What are the key health indicators you monitor for each CyberArk
   component (Vault, CPM, PVWA, PSM)? Name the specific tool or location
   in PVWA where you check each component's health.
2. Walk through investigating the {num_failed_accounts} CPM errors.
   What logs would you check, in what order, and what are the most
   common root causes?
3. The PSM server is showing degraded performance. What are the common
   causes of PSM performance issues and how do you diagnose them?
   What performance counters are most relevant?
4. Describe the CyberArk backup process. What must be backed up, how
   often, and where are backup files stored? What is the difference
   between a Vault backup and a Safe export?
5. You need to perform a CyberArk version upgrade. What is the correct
   upgrade sequence for the components and why does order matter?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Enterprise", "Northwind Global", "Alpine Industries"],
            "num_vaults": ["2", "4", "2", "3"],
            "num_cpms": ["2", "4", "3", "6"],
            "num_pvwas": ["3", "6", "4", "8"],
            "num_psms": ["2", "4", "3", "6"],
            "num_accounts": ["5,000", "15,000", "3,500", "22,000"],
            "num_failed_accounts": ["45", "120", "28", "200"],
        },
        "exam_objectives": ["3.1", "3.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA3-001: CyberArk System Health and Monitoring

Q1 ??" Health monitoring per component
Vault: PVWA ??' Administration ??' System Health ??' Vault status.
Check: Vault service running, disk space (Vault storage), replication
status to DR Vault, CyberArk Event Notification Engine (ENE) status.
CPM: PVWA ??' Administration ??' System Health ??' CPM status.
Check: CPM service running, last scan time, number of accounts with errors,
CPMLog on the CPM server (C:/Program Files/CyberArk/Password Manager/Logs).
PVWA: IIS Application Pool status, Windows Event Log, PVWA log files
(C:/CyberArk/Password Vault Web Access/Logs).
PSM: PVWA ??' Administration ??' System Health ??' PSM status.
Check: PSM service, active sessions count, available capacity,
PSMLog (C:/Program Files/CyberArk/PSM/Logs).

Q2 ??" Investigating CPM errors
Order of investigation:
1. PVWA ??' Accounts ??' filter by CPM Status = Error ??' review error message
   on each account (hover over error icon for details)
2. CPM server ??' C:/Program Files/CyberArk/Password Manager/Logs/CPMLog.log
   ??' search for the account name ??' find specific error message
3. Common root causes and fixes:
   - "Logon failure" ??' password changed manually, trigger Reconcile
   - "Access denied" ??' CPM service account lost permissions, re-grant
   - "RPC unavailable" ??' target machine offline or firewall blocking
   - "Account locked" ??' unlock in AD, check why it's locking
   - "Platform mismatch" ??' wrong platform assigned, reassign correct one
4. For bulk failures on the same subnet: check network/firewall changes

Q3 ??" PSM performance issues
Common causes:
  - Too many concurrent sessions (check licence limit vs active sessions)
  - Insufficient CPU/RAM on PSM server (check Windows Performance Monitor)
  - Disk I/O bottleneck (session recordings filling disk)
  - Windows RDS licensing issues
Relevant performance counters:
  - CPU: % Processor Time (should be under 80%)
  - Memory: Available MBytes (should not be near zero)
  - Disk: Avg Disk Queue Length (over 2 = bottleneck)
  - RDS: Active Sessions (check against PSM licence capacity)
Diagnosis: PVWA ??' System Health ??' PSM ??' check active session count vs
capacity. Remote into PSM server ??' Task Manager ??' Resource Monitor.

Q4 ??" CyberArk backup process
What to back up:
  - Vault data: automatic, configured in DBParm.ini (BackupKey and SafeBackupPath)
  - Vault server itself: OS-level backup of the Vault server
  - PVWA configuration: web.config and CyberArk configuration files
  - CPM configuration: policy files and configuration
  - PSM configuration: PSMConfigParameters.ini and connection components
Vault backup runs automatically and stores encrypted backup files to the
configured backup location. Frequency: typically daily minimum.
Vault backup vs Safe export: Vault backup = entire Vault encrypted backup
for DR purposes. Safe export = exports accounts from a specific Safe to
a file for migration or selective restore ??" not a full backup.

Q5 ??" Upgrade sequence
Correct upgrade order:
1. Digital Vault (Primary) ??" always first, new Vault features are required
2. Digital Vault (DR) ??" replicate Vault version
3. CPM ??" depends on Vault API compatibility
4. PVWA ??" depends on Vault API compatibility
5. PSM ??" depends on Vault and PVWA
6. AIM/AAM components ??" last
Why order matters: each component has API compatibility requirements with
the Vault. Upgrading components before the Vault can break communication.
Always check the CyberArk compatibility matrix before upgrading.
Always test in a non-production environment first.
"""
    },
    {
        "id": "CA3-002",
        "domain": "3",
        "sub_topic": "Safe Management and Maintenance",
        "objective": "3.2 - Perform Safe management and maintenance tasks",
        "scenario_template": """
You are performing quarterly maintenance for CyberArk at {org_name}.
Tasks include:

  - {num_stale} accounts have not been accessed in over {stale_days} days
  - {num_safes} Safes have no owner assigned
  - A Safe called "{safe_name}" has grown to {safe_size} GB and is
    causing Vault storage concerns
  - {num_orphan} accounts belong to terminated employees' personal Safes
  - The DR Vault has not been tested in {dr_days} days

Questions:
1. How do you identify and handle the {num_stale} stale accounts?
   What report in PVWA shows account last access time? What are your
   options: delete, disable, or retain with justification?
2. The {num_safes} Safes with no owner are a governance risk. How do
   you find them and what is the process for assigning ownership?
   What are the risks of ownerless Safes?
3. "{safe_name}" has grown to {safe_size} GB. What is causing this growth
   and how do you reduce the Safe size? What are your options for
   archiving or managing Safe content?
4. Walk through the process of deleting a Safe safely. What must you
   verify before deletion and what happens to accounts inside?
5. The DR Vault has not been tested in {dr_days} days. Describe the
   DR Vault failover test process and what you verify to confirm the
   DR Vault is functioning correctly.
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Ltd", "Northwind Bank", "Pacific Corp"],
            "num_stale": ["234", "89", "567", "145"],
            "stale_days": ["90", "180", "60", "365"],
            "num_safes": ["12", "34", "7", "28"],
            "safe_name": ["ITAdmins-Prod", "ServiceAccounts-Legacy", "WindowsAdmins-DC", "DBAccounts-Finance"],
            "safe_size": ["45", "120", "28", "200"],
            "num_orphan": ["23", "67", "11", "45"],
            "dr_days": ["180", "365", "90", "270"],
        },
        "exam_objectives": ["3.2", "3.3"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA3-002: Safe Management and Maintenance

Q1 ??" Stale account management
Report: PVWA ??' Reports ??' Privileged Accounts Inventory ??' filter by
Last Password Used date. Export to CSV for analysis.
Also: PVWA ??' Accounts ??' Advanced filter ??' Last Used before [date].
Options for stale accounts:
  - Disable: deactivate the account in CyberArk (not deleted ??" retained
    for audit trail). Use for accounts that may be needed again.
  - Delete: remove permanently from CyberArk. Only after confirming the
    account is no longer needed and has been disabled in the target system.
  - Retain with justification: document in Safe description why the
    account must be retained despite no recent use (e.g. DR accounts).
Best practice: never delete without confirming with the account owner first.

Q2 ??" Ownerless Safes
Find: PVWA ??' Safes ??' review Safe Members for each Safe ??" look for Safes
with no user or group in the Owner role.
Or use the CyberArk REST API to list all Safes and their members programmatically.
Process for assigning ownership:
  1. Identify the business unit responsible for the accounts in the Safe
  2. Contact the business unit to designate a Safe Owner
  3. Add the designated owner with Owner permissions in Safe Members
Risks of ownerless Safes:
  - No accountability for who has access
  - Access requests cannot be properly approved
  - Compliance violations (SOX, ISO 27001 require access owners)
  - Accounts may be left unreviewed and unmanaged

Q3 ??" Large Safe size management
Cause of growth: primarily session recordings (PSM recordings stored
in the Safe grow continuously). Also: old account versions and history.
Options to reduce size:
  1. Configure PSM recording retention policy ??" automatically delete
     recordings older than X days (set in PSM configuration)
  2. Move old recordings to external storage (NAS/Azure Blob)
  3. Review and archive accounts no longer in use
  4. Configure Safe quota in Vault configuration to alert before limit
Safe size is managed via Vault storage ??" check DBParm.ini for storage
path and ensure adequate disk space on the Vault server.

Q4 ??" Safe deletion process
Before deleting a Safe:
  1. Verify all accounts inside are no longer needed (confirm with owners)
  2. Delete or move all accounts out of the Safe first
  3. Remove all Safe Members
  4. Confirm no active CPM/PSM dependencies on this Safe
  5. Check audit log ??" ensure no recent access that would indicate active use
Process: PVWA ??' Safes ??' [Safe] ??' Delete Safe.
Note: you cannot delete a Safe that still contains accounts. CyberArk
will prevent deletion until the Safe is empty.
What happens to accounts: you must manually delete or move accounts first ??"
Safe deletion does not cascade-delete accounts (a safety feature).

Q5 ??" DR Vault failover test
Process:
  1. Confirm replication is current: Primary Vault ??' check replication
     log to confirm DR Vault is fully synchronised
  2. Stop the Primary Vault service (controlled test)
  3. On DR Vault: verify all CyberArk services start correctly
  4. Update DNS or load balancer to point CyberArk components at DR Vault
  5. Test: log into PVWA ??' verify accounts are visible and accessible
  6. Test CPM: verify a password change completes successfully
  7. Test PSM: initiate a test session through the DR environment
  8. Document: record RTO achieved, any issues found
  9. Fail back: stop DR Vault services ??' restart Primary ??' re-sync ??' repoint DNS
Verify: all components (CPM, PVWA, PSM) reconnect to Primary successfully
after failback. Check replication resumes.
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 4 ??" PASSWORD MANAGEMENT CONFIGURATION
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN4_SCENARIOS = [
    {
        "id": "CA4-001",
        "domain": "4",
        "sub_topic": "CPM Password Management and Platform Configuration",
        "objective": "4.1 - Configure password management policies and platforms",
        "scenario_template": """
You are configuring password management for {org_name}'s CyberArk environment.
The security team has defined the following requirements:

  - Windows local admin passwords must rotate every {win_rotation} days
  - Unix root passwords must rotate every {unix_rotation} days
  - {app_type} service account passwords must NOT rotate automatically
    (application restarts required and must be planned)
  - Passwords must meet complexity: {complexity_req}
  - Failed rotation must trigger an alert within {alert_time} minutes
  - Reconcile accounts must be configured for Windows domain accounts

Questions:
1. Explain the difference between Verify, Change, and Reconcile in CyberArk
   CPM password management. When does each operation trigger and what
   happens if each one fails?
2. Configure a Windows platform policy for {win_rotation}-day rotation
   with the specified complexity. Walk through the specific settings in
   Platform Management you would modify.
3. The {app_type} service accounts must NOT auto-rotate. How do you
   configure CyberArk to manage these passwords (store and control access)
   without automatic rotation? What setting controls this?
4. Configure a Reconcile account for Windows domain accounts.
   What is a Reconcile account, what permissions does it need, and
   when does CyberArk use it automatically?
5. Design the alerting configuration for failed password rotations.
   What CyberArk component sends alerts, how do you configure it,
   and what notification methods are available?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Enterprise", "Northwind Global", "Alpine Industries"],
            "win_rotation": ["30", "60", "90", "45"],
            "unix_rotation": ["30", "90", "60", "45"],
            "app_type": ["SAP", "Oracle Middleware", "WebSphere", "IIS Application Pool"],
            "complexity_req": [
                "minimum 20 characters, upper/lower/number/special",
                "minimum 16 characters, no dictionary words",
                "minimum 24 characters, all character types required",
            ],
            "alert_time": ["15", "30", "5", "60"],
        },
        "exam_objectives": ["4.1", "4.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA4-001: CPM Password Management Configuration

Q1 ??" Verify, Change, and Reconcile
Verify: CPM logs into the target system to confirm the current password
in the Vault still works. Does NOT change the password. Fails if Vault
password doesn't match the actual password on the system.
Change: CPM generates a new password and changes it on the target system,
then stores the new password in the Vault. This is the rotation operation.
Fails if CPM cannot authenticate or change the password on the target.
Reconcile: CPM uses a separate Reconcile account (with higher privileges)
to reset the account's password and update the Vault. Used when Verify
fails (passwords are out of sync) and the CPM cannot log in with the
current Vault password. The Reconcile account acts as a "password reset" mechanism.
Trigger: Verify runs on schedule (e.g. daily). Change runs on the rotation
schedule. Reconcile runs automatically when Verify fails, or can be triggered manually.

Q2 ??" Windows platform configuration for rotation
PVWA ??' Administration ??' Platform Management ??' WinServerLocal ??' Edit.
Settings to modify:
  - Password Settings:
    Minimum password length: set to required minimum
    Required character sets: enable Uppercase, Lowercase, Digits, Special
    Allowed/Required special chars: define specific characters
  - Automatic Password Management:
    Allow automatic password management: Yes
    Password change interval: set to rotation days (e.g. 30)
    Password verification interval: set to verify frequency (e.g. 7 days)
  - Immediate change: Yes (change immediately on first management)
Save and assign to affected accounts.

Q3 ??" Disabling automatic rotation for service accounts
PVWA ??' Platform Management ??' [Service Account Platform] ??' Edit.
Automatic Password Management section:
  - Allow automatic password management: set to NO
This stores the password in the Vault and controls who can access it,
but the CPM will NOT rotate it automatically.
Users must use the "Change" button in PVWA manually when a planned
rotation is scheduled (coordinated with the application team).
Alternatively: set a very long rotation interval (e.g. 9999 days) as
a practical workaround while keeping the feature technically enabled.

Q4 ??" Reconcile account configuration
Reconcile account: a highly privileged account (e.g. Domain Admin for
Windows, or a local account with password reset rights) stored in CyberArk
that the CPM uses to reset another account's password when it cannot
log in with the current Vault password.
Required permissions for the Reconcile account:
  - Windows domain: Domain Admin or Account Operators (ability to reset passwords)
  - Windows local: local Administrator on the target machine
  - Must be stored in the Vault in its own Safe (separate from managed accounts)
Configuration: in Platform Management ??' Reconciliation section ??'
set the Reconcile account Safe and account name.
CyberArk triggers Reconcile automatically when: Verify fails AND Change
fails ??" indicating passwords are out of sync.

Q5 ??" Alert configuration for failed rotations
Component: CyberArk Event Notification Engine (ENE) ??" Windows service
on the Vault server that sends notifications.
Configuration: PVWA ??' Administration ??' Notifications ??' configure email
settings (SMTP server, sender address, recipient addresses).
Notification triggers to configure:
  - CPM Error: account password change failed
  - CPM Warning: account not changed within expected interval
Notification methods available:
  - Email (SMTP) ??" primary method
  - SNMP traps ??" for integration with network monitoring tools
  - Syslog ??" for SIEM integration
  - CyberArk dashboard alerts ??" visible in PVWA System Health
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 5 ??" SECURITY AND AUDIT
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN5_SCENARIOS = [
    {
        "id": "CA5-001",
        "domain": "5",
        "sub_topic": "Vault Security and Audit Reporting",
        "objective": "5.1 - Configure security settings and generate audit reports",
        "scenario_template": """
{org_name} is preparing for a {audit_type} audit. The auditors require
evidence of privileged access controls. You have {days_to_audit} days
to prepare.

Audit requirements:
  - List of all privileged accounts managed in CyberArk
  - Evidence that passwords are rotated per policy
  - All access to privileged accounts for the past {audit_period} months
  - Evidence of dual control enforcement for {sensitive_safe} accounts
  - Proof that all PSM sessions are recorded

Questions:
1. Generate the Privileged Accounts Inventory report. What does this report
   show, where do you access it, and how do you export it for the auditors?
2. The auditors want evidence of password rotation compliance. Which report
   shows password change history and rotation dates? Walk through generating
   and exporting it.
3. Generate an access report showing who accessed what accounts during the
   {audit_period}-month period. What CyberArk report provides this and
   what does it include?
4. Explain Dual Control in CyberArk. How do you configure it for the
   {sensitive_safe} Safe and what is the user experience when Dual Control
   is enforced?
5. How do you prove to auditors that all PSM sessions are recorded?
   Where are recordings stored and how can an auditor play back a specific
   session? What metadata is captured with each recording?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Finance", "Northwind Bank", "Alpine Healthcare"],
            "audit_type": ["SOX", "PCI DSS", "ISO 27001", "HIPAA"],
            "days_to_audit": ["14", "30", "7", "45"],
            "audit_period": ["3", "6", "12", "9"],
            "sensitive_safe": ["Finance-Admins", "DomainControllers", "PayrollSystem", "CoreBanking"],
        },
        "exam_objectives": ["5.1", "5.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA5-001: Vault Security and Audit Reporting

Q1 ??" Privileged Accounts Inventory report
Path: PVWA ??' Reports ??' Privileged Accounts Inventory.
Shows: all accounts managed in CyberArk, including Safe name, account name,
address, platform, CPM status, last password change date, last access date.
Export: click "Export to CSV" ??" provides a spreadsheet suitable for auditors.
Filter options: by Safe, platform, CPM status, or date range before exporting.

Q2 ??" Password rotation compliance report
Path: PVWA ??' Reports ??' Privileged Accounts Compliance.
This report shows: accounts that have and haven't been changed within their
required rotation interval. Shows last change date vs policy requirement.
For detailed history: PVWA ??' Reports ??' Activity Log ??' filter by activity
type = "Change password" ??' set date range ??' export.
This provides a time-stamped record of every password change for every account.

Q3 ??" Access report (who accessed what)
Path: PVWA ??' Reports ??' Activity Log (also called Audit Log).
Filter: date range = audit period, Activity type = "Retrieve password" or
"Connect" (for PSM sessions).
Report includes: timestamp, user who accessed, account accessed, Safe name,
IP address of user, workstation name, reason provided (if reason required).
Export to CSV for auditors. This is the primary privileged access audit trail.

Q4 ??" Dual Control configuration
Dual Control: requires a second authorized user to approve access to an
account before the requester can retrieve or use the password.
Configuration: PVWA ??' Safes ??' [sensitive Safe] ??' Safe Members ??'
[User/Group] ??' Edit Permissions ??' Enable "Require dual control password
access approval" checkbox.
Also configure who can approve: add an Approver group with the
"Approve requests" permission on the Safe.
User experience: requester clicks "Connect" or "Retrieve" ??' system shows
"Request pending approval" ??' approver receives notification ??' approver
logs in and approves ??' requester is then granted access (time-limited).
Auditors can see both the request and the approval in the Activity Log.

Q5 ??" Proving PSM session recording
PSM recordings are stored: in a dedicated PSM recordings Safe in the Vault
(typically named "PSMRecordings" or configured in PSM settings).
Every PSM session automatically generates a recording ??" no opt-out.
To prove to auditors:
  PVWA ??' Reports ??' Sessions Monitoring (or Activity Log filtered by PSM sessions).
  Shows: session ID, user, target account, target server, start/end time, duration.
Playback: PVWA ??' Session Monitoring ??' find session ??' click Play.
Auditors can watch the entire session recording through the PVWA browser.
Metadata captured with each recording:
  - User who initiated the session
  - Target account and address
  - Start time, end time, duration
  - Commands typed (if text recording enabled)
  - Keystroke log (if configured)
  - All screen activity (video recording)
"""
    },
    {
        "id": "CA5-002",
        "domain": "5",
        "sub_topic": "Master Policy and Safe Security Settings",
        "objective": "5.2 - Configure Master Policy and Safe security controls",
        "scenario_template": """
You are reviewing security configurations at {org_name}.
A recent security assessment identified the following gaps:

  - The Master Policy has not been reviewed since CyberArk was deployed
    {years_ago} years ago
  - {num_safes_no_reason} Safes do not require users to provide a reason
    before accessing accounts
  - Exclusive access is not enforced on {critical_safe} (the most
    sensitive Safe in the environment)
  - Session recording is not mandatory for {unrecorded_platform} connections
  - The Vault network firewall rules have not been reviewed

Questions:
1. What is the Master Policy in CyberArk and what does it control?
   How does the Master Policy interact with Safe-level settings?
   Which takes precedence?
2. Configure "Require reason" for password access on the {critical_safe}
   Safe. Walk through the specific setting and explain how the reason
   is captured in the audit log.
3. Explain Exclusive Access in CyberArk. How do you enable it on the
   {critical_safe} Safe, and what is the user experience when it is enabled?
4. Configure mandatory session recording for {unrecorded_platform}
   connections through PSM. Where is this setting and how does it interact
   with the platform configuration?
5. What are the recommended network security controls for the CyberArk
   Vault server? List the specific ports and protocols that should be
   allowed and from which sources.
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Bank", "Northwind Gov", "Pacific Systems"],
            "years_ago": ["3", "5", "2", "7"],
            "num_safes_no_reason": ["24", "67", "11", "43"],
            "critical_safe": ["DomainControllers-Prod", "CoreBanking-Admins", "PayrollSystem", "FirewallAdmins"],
            "unrecorded_platform": ["SSH (Unix)", "RDP (Windows)", "Telnet (Network)", "SQL (Database)"],
        },
        "exam_objectives": ["5.2", "5.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE ??" CA5-002: Master Policy and Safe Security Settings

Q1 ??" Master Policy overview
The Master Policy is the global security policy in CyberArk that defines
default behaviours for all Safes and accounts in the Vault.
It controls: whether passwords are managed automatically, whether reasons
are required for access, session recording defaults, dual control defaults,
exclusive access defaults, and more.
Interaction with Safe settings: Safe-level settings can OVERRIDE the Master
Policy for specific Safes ??" but only if the Master Policy allows exceptions.
Precedence: Master Policy sets the floor. If Master Policy says "Require
reason: Yes (mandatory)" then NO Safe can turn it off. If Master Policy
says "Require reason: Active" (allows exceptions), then individual Safes
can turn it on or off.
Path: PVWA ??' Administration ??' Master Policy.

Q2 ??" Require reason configuration
Path: PVWA ??' Safes ??' [critical Safe] ??' Edit Safe ??' Security section ??'
"Require users to specify a reason for access" ??' set to Yes.
User experience: when a user clicks Retrieve or Connect, a dialog box
appears requiring them to type a reason before proceeding.
Audit log: the reason is captured in the Activity Log with the timestamp,
user, account accessed, and the typed reason. Auditors can filter by
reason content or search for blank reasons.

Q3 ??" Exclusive Access
Exclusive Access: only one user can check out and use a password at a time.
When User A has the account checked out, no other user can retrieve or use
it until User A checks it back in (or the exclusive access time expires).
Enable: PVWA ??' Safes ??' [critical Safe] ??' Edit Safe ??' Access section ??'
"Enforce exclusive access" ??' set to Yes. Set the maximum exclusive period.
User experience: User A checks out account ??' status shows "In use by [User A]"
??' User B attempts access ??' sees "Account is currently in use" message ??'
must wait or request emergency override (Vault Admin can force release).
Use case: critical accounts (domain admin, root) where concurrent use
creates accountability and security concerns.

Q4 ??" Mandatory session recording for PSM
Path: PVWA ??' Administration ??' Platform Management ??' [Platform] ??' UI &
Workflows ??' Required Properties ??' Session recording.
Set: "Record and save session activity" ??' Mandatory.
Also: Master Policy ??' Session Management ??' "Record and save session activity"
??' set to Active/Mandatory for global enforcement.
Platform interaction: if the platform requires recording and PSM is configured
as the connection method, every session through that platform is recorded
automatically. Users cannot connect without recording being active.

Q5 ??" Vault network security controls
Recommended firewall rules for the Vault server:
INBOUND (allowed):
  - Port 1858 (TCP): from CPM, PVWA, PSM, AIM servers ??" Vault communication
  - Port 443 (HTTPS): from admin workstations for Vault administration only
  - RDP (3389): from dedicated admin jump server only (not open internet)
OUTBOUND (allowed):
  - Port 25 (SMTP): to mail server for ENE notifications
  - DNS: to DNS server
  - NTP: to time server (critical for audit log integrity)
DENY ALL ELSE: the Vault server should have NO other inbound or outbound
connectivity. It should never browse the internet or communicate with
unapproved systems. This is the most hardened server in the environment.
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 6 ??" SESSION MANAGEMENT CONFIGURATION
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN6_SCENARIOS = [
    {
        "id": "CA6-001",
        "domain": "6",
        "sub_topic": "PSM Configuration and Session Management",
        "objective": "6.1 - Configure PSM for privileged session management and recording",
        "scenario_template": """
You are configuring the Privileged Session Manager (PSM) at {org_name}.
The environment requires:

  - RDP connections to {num_windows_servers} Windows servers via PSM
  - SSH connections to {num_unix_servers} Unix/Linux servers via PSM
  - Database connections to {num_db_servers} SQL Server instances via PSM
  - All sessions must be recorded and stored for {retention_days} days
  - Users must connect through PSM only ??" direct RDP/SSH is blocked by firewall
  - {exec_team} users require transparent (seamless) PSM connections

Questions:
1. Explain the PSM connection flow from the user's perspective. What happens
   from the moment a user clicks "Connect" in PVWA to when they are
   connected to the target server?
2. Configure PSM to support RDP connections via the "Connect" button in PVWA
   and via an RDP client (PSM for Windows). What are the two methods and
   what CyberArk component enables each?
3. Configure PSM for SSH connections to the {num_unix_servers} Unix servers.
   What is PSM for SSH (PSMP) and how does it differ from standard PSM?
   What are the connection string requirements?
4. The {exec_team} users want transparent connections ??" they want to launch
   sessions without seeing the PVWA interface. What CyberArk feature enables
   this and how do you configure it?
5. Session recordings are stored for {retention_days} days. Configure the
   retention policy and explain the storage implications. How does CyberArk
   handle recordings when storage is near capacity?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Enterprise", "Northwind Tech", "Alpine Global"],
            "num_windows_servers": ["200", "500", "80", "1,200"],
            "num_unix_servers": ["150", "300", "60", "800"],
            "num_db_servers": ["30", "80", "15", "200"],
            "retention_days": ["90", "365", "180", "730"],
            "exec_team": ["DevOps", "DBA", "Network Operations", "Security Operations"],
        },
        "exam_objectives": ["6.1", "6.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA6-001: PSM Configuration and Session Management

Q1 ??" PSM connection flow
1. User logs into PVWA and navigates to the target account
2. User clicks "Connect" ??" PVWA contacts the Vault to retrieve credentials
3. PVWA instructs PSM to initiate a session
4. PSM retrieves the credentials from the Vault (PSM never shows them to the user)
5. PSM connects to the target server using the retrieved credentials
6. PSM establishes a session (RDP, SSH, etc.) on behalf of the user
7. PSM proxies the session ??" user interacts through PSM, never seeing the password
8. PSM records all session activity
9. On disconnect, PSM terminates the session and saves the recording to the Vault
Key point: the user NEVER sees or handles the actual password at any point.

Q2 ??" PSM RDP connection methods
Method 1 ??" "Connect" button in PVWA:
  User clicks Connect in PVWA ??' PVWA launches an RDP file ??' user's RDP client
  connects to the PSM server ??' PSM proxies to the target.
  This uses the PSM server's RDP listener (port 3389).
  Connection component: PSM-RDP (configured in Platform Management ??' UI & Workflows).
Method 2 ??" PSM for Windows (RDP client method):
  User opens their RDP client directly ??' connects to PSM server ??' PSM
  authenticates the user and presents a menu of available target systems.
  Uses PSMConnect and PSMAdminConnect accounts on the PSM server.

Q3 ??" PSM for SSH (PSMP)
PSMP is a separate Linux-based component that acts as an SSH proxy.
Difference from standard PSM (Windows-based RDP proxy):
  - PSMP runs on Linux (not Windows)
  - Handles SSH protocol natively
  - Users SSH into PSMP, which then SSHs to the target
  - Records SSH sessions (text-based, keystroke logging)
Connection string format: [vault_user]@[target_user]@[target_address]@[psmp_server]
Example: john@root@webserver01.contoso.com@psmp.contoso.com
The user SSHs to PSMP with this format ??" PSMP parses it, authenticates
the user against the Vault, retrieves the root credential, and connects.

Q4 ??" Transparent (seamless) PSM connections
Feature: PSM URL (direct connection URL) or CyberArk HTML5 Gateway.
Also: PSM for Web / CyberArk Alero for browser-based transparent access.
For DevOps/DBA teams: configure Connection Component to launch transparently
using a URL scheme (e.g. PSM:// or SSH:// links that launch directly).
Configuration: Platform Management ??' Connection Components ??' configure
"PSM Launch Method" ??' set to "Transparent" or configure the URL directly.
Users bookmark or script the URL and click it ??" no PVWA browsing required.
CyberArk Alero: provides zero-client seamless access for third parties
and internal teams via browser without any installed client.

Q5 ??" Recording retention configuration
Path: PSM server configuration ??' PSMConfigParameters.ini ??'
RecordingRetentionPeriod = [number of days].
Also configurable via PVWA ??' Administration ??' Options ??' Session Management
??' Recording retention policy.
Storage implications: video recordings are large ??" estimate 50-200MB per
hour of session depending on resolution and activity. For 365 days, calculate:
average sessions/day ?-- average duration ?-- storage per hour.
When storage is near capacity: CyberArk raises a Vault storage warning alert
via ENE. The PSM will eventually stop recording new sessions if storage is
full ??" this is a critical alert that must be monitored.
Best practice: dedicate a separate large volume for PSM recordings, monitor
storage usage, and implement auto-archival to cheaper storage (e.g. NAS, Azure Blob).
"""
    },
    {
        "id": "CA6-002",
        "domain": "6",
        "sub_topic": "PSM Session Monitoring and Termination",
        "objective": "6.2 - Monitor active PSM sessions and configure session controls",
        "scenario_template": """
You are the CyberArk administrator on duty at {org_name}. During a routine
check, you notice the following in the Session Monitoring dashboard:

  - {num_active} active PSM sessions currently running
  - User {suspicious_user} has been connected to {critical_server} for
    {session_duration} hours ??" unusually long
  - {suspicious_user}'s session shows {suspicious_activity} in the live view
  - A session from IP {unknown_ip} was initiated {time_ago} minutes ago
    to a Domain Controller ??" this IP is not recognised
  - {num_idle} sessions have been idle for over {idle_time} minutes

Questions:
1. Walk through how you would investigate {suspicious_user}'s session
   in real time using PVWA Session Monitoring. What information is
   visible in the live session view?
2. You determine {suspicious_user}'s session is suspicious. How do you
   terminate an active PSM session from PVWA? What happens to the user
   and the session recording when you terminate it?
3. The session from {unknown_ip} to a Domain Controller is a potential
   security incident. What immediate steps do you take and what information
   from the session monitoring helps your investigation?
4. Configure an automatic session termination policy for idle sessions.
   Where is this setting and what is the recommended idle timeout for
   privileged sessions?
5. Describe how PSM's "Suspend Session" feature works and when you would
   use it vs immediate termination. What is the user experience during
   a suspended session?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Bank", "Northwind Tech", "Pacific Systems"],
            "num_active": ["34", "87", "12", "156"],
            "suspicious_user": ["jsmith", "a.jones", "mwilson", "t.brown"],
            "critical_server": ["DC01.contoso.local", "SQL-PROD-01", "FW-CORE-01", "PAYROLL-SRV"],
            "session_duration": ["6", "12", "4", "8"],
            "suspicious_activity": [
                "bulk file copying to a USB drive",
                "running PowerShell scripts and exporting AD data",
                "modifying firewall rules",
                "accessing payroll database tables",
            ],
            "unknown_ip": ["10.50.33.44", "192.168.77.201", "172.16.50.99", "10.100.5.22"],
            "time_ago": ["12", "5", "25", "3"],
            "num_idle": ["8", "23", "4", "15"],
            "idle_time": ["60", "120", "90", "30"],
        },
        "exam_objectives": ["6.2", "6.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE ??" CA6-002: PSM Session Monitoring and Termination

Q1 ??" Live session investigation in PVWA
Path: PVWA ??' Monitoring ??' Active Sessions (or Session Monitoring dashboard).
Click on the suspicious user's session to view:
  - Live screen feed (video of what the user is doing right now)
  - Session metadata: user, target account, target server, start time, duration
  - Keystroke log (if text recording enabled) ??" shows commands typed
  - File transfer activity (if monitored)
  - Mouse/keyboard activity indicators
You can watch the session in real time without the user knowing.
This is your primary investigation tool for live suspicious activity.

Q2 ??" Terminating an active PSM session
Path: PVWA ??' Monitoring ??' Active Sessions ??' find the session ??' click
"Terminate" button.
What happens to the user: their session is immediately disconnected. They
see a standard RDP/SSH disconnection message ??" no warning is given.
What happens to the recording: CyberArk saves and closes the recording
up to the point of termination. The partial recording is stored in the
Vault and is fully playable. The termination event is logged in the Audit Log
with the terminating admin's username, timestamp, and reason (if entered).

Q3 ??" Responding to unknown IP session on Domain Controller
Immediate steps:
1. PVWA ??' Active Sessions ??' find the session from unknown IP ??' view live
2. If clearly unauthorised: terminate the session immediately
3. PVWA ??' Activity Log ??' find the session initiation ??' note: which CyberArk
   user account was used to initiate the session
4. Determine if the CyberArk user account was compromised: check their
   recent login history and location
5. Lock the CyberArk user account immediately if compromised
6. Escalate to incident response team ??" potential account compromise
7. Preserve the session recording as forensic evidence (do not delete)
Information from session monitoring for investigation:
  - CyberArk username that initiated the session
  - Exact start time of the session
  - The target Domain Controller and account used
  - Live recording of all actions taken

Q4 ??" Automatic idle session termination
Path: PVWA ??' Administration ??' Options ??' Session Management ??'
"Disconnect idle session after" ??' set to recommended timeout (e.g. 15-30 minutes).
Also configurable per platform: Platform Management ??' [Platform] ??'
Connection Components ??' disconnect idle sessions.
Recommended timeout for privileged sessions: 15 minutes maximum.
Rationale: an unattended privileged session on a Domain Controller or
critical server is a significant security risk ??" an attacker with physical
or remote access to the admin's workstation can use it.

Q5 ??" Suspend Session vs Termination
Suspend Session: pauses the session ??" the user's screen is locked and they
cannot interact with the target. The session remains connected in the background.
A Vault Admin can resume or terminate the suspended session.
User experience during suspension: their screen goes black or shows a
"Session suspended by administrator" message. They cannot type or click.
Use Suspend when:
  - You want to investigate further before deciding to terminate
  - You want to warn the user and give them a chance to explain
  - You need to pause activity while escalating to management
Use Termination when:
  - The activity is clearly malicious or unauthorised
  - No investigation needed ??" immediate action required
  - The session poses an immediate risk to the environment
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  DOMAIN 7 ??" USER MANAGEMENT CONFIGURATION
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

DOMAIN7_SCENARIOS = [
    {
        "id": "CA7-001",
        "domain": "7",
        "sub_topic": "CyberArk User Management and LDAP Integration",
        "objective": "7.1 - Configure user management and LDAP/AD directory integration",
        "scenario_template": """
You are configuring user management for CyberArk at {org_name}.
The organisation has {num_cyberark_users} users who need CyberArk access
across {num_departments} departments.

Current requirements:
  - All users must authenticate using their Active Directory credentials
  - {num_vault_admins} Vault Administrators need full administrative access
  - {num_safe_managers} Safe Managers need to manage specific Safes only
  - {num_end_users} end users need access to retrieve passwords only
  - User provisioning must be automated via AD group membership
  - MFA must be enforced for all {num_vault_admins} Vault Administrators

Questions:
1. Configure LDAP integration between CyberArk and Active Directory.
   Walk through the steps in PVWA and explain what the LDAP integration
   enables. What account does CyberArk use to bind to AD?
2. Explain the difference between CyberArk Vault users and LDAP-mapped users.
   What are the advantages of using LDAP-mapped users over creating local
   Vault users?
3. Design the CyberArk group structure for the three user types above.
   What built-in CyberArk groups exist and which would you use for each role?
4. Configure MFA for the {num_vault_admins} Vault Administrators in CyberArk.
   What MFA options does CyberArk support natively and what third-party
   integrations are available?
5. A user has left the organisation. Walk through the offboarding process
   in CyberArk. What must be done to ensure their access is fully revoked?
   What happens to the Safes they owned?
""",
        "variables": {
            "org_name": ["Contoso Corp", "Fabrikam Enterprise", "Northwind Global", "Alpine Systems"],
            "num_cyberark_users": ["150", "400", "80", "800"],
            "num_departments": ["6", "12", "4", "20"],
            "num_vault_admins": ["4", "8", "3", "12"],
            "num_safe_managers": ["15", "40", "8", "60"],
            "num_end_users": ["131", "352", "69", "728"],
        },
        "exam_objectives": ["7.1", "7.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE ??" CA7-001: CyberArk User Management and LDAP Integration

Q1 ??" LDAP integration configuration
Path: PVWA ??' Administration ??' LDAP Integration ??' Add LDAP Directory.
Configuration fields:
  - Directory name: friendly name (e.g. "Contoso AD")
  - Hosts: AD domain controller IP/FQDN (primary and secondary)
  - Port: 389 (LDAP) or 636 (LDAPS ??" recommended)
  - Bind account: a dedicated low-privilege AD service account used by
    CyberArk to query the directory (read-only, no admin rights needed)
  - Base context: the AD OU to search (e.g. DC=contoso,DC=com)
  - SSL: enable for LDAPS (secure)
What LDAP integration enables:
  - Users authenticate with their AD credentials (no separate Vault password)
  - CyberArk groups can be mapped to AD groups (automatic provisioning)
  - User attributes (email, display name) pulled from AD automatically

Q2 ??" Vault users vs LDAP-mapped users
Vault users: created and managed directly in CyberArk. Have a separate
Vault password. Must be manually created and deleted. No AD synchronisation.
LDAP-mapped users: authenticated via AD. CyberArk maps an AD group to a
CyberArk group ??" any AD group member automatically gets CyberArk access.
Advantages of LDAP-mapped users:
  - Single password (AD credentials ??" no Vault password to manage)
  - Automatic provisioning: add user to AD group ??' they get CyberArk access
  - Automatic deprovisioning: remove from AD group ??' access revoked
  - Enforces existing AD MFA/conditional access policies
  - Scales easily ??" no manual Vault user creation needed
Best practice: use LDAP-mapped users for all standard users. Keep a small
number of local Vault users only for break-glass/emergency access.

Q3 ??" CyberArk group structure
Built-in CyberArk groups:
  - Vault Admins: full administrative access to the Vault (use sparingly)
  - Auditors: read-only access to all Safes for audit purposes
  - Safe Managers (custom): create per-Safe owner groups
  - End Users (custom): create per-team access groups
Design for this environment:
  - Vault Administrators ??' map to AD group "CyberArk-VaultAdmins"
    ??' assign to built-in Vault Admins group
  - Safe Managers ??' map to AD group "CyberArk-SafeManagers"
    ??' grant Owner permissions on specific Safes only
  - End Users ??' map to AD groups per team (e.g. "CyberArk-Finance-Users")
    ??' grant Use/Retrieve permissions on relevant Safes only

Q4 ??" MFA for Vault Administrators
Native CyberArk MFA: PVWA supports RADIUS-based MFA natively.
Configure: PVWA ??' Administration ??' Authentication Methods ??' RADIUS.
Enter RADIUS server IP, port (1812), shared secret.
Map Vault Admin users to use RADIUS authentication method.
Third-party integrations available:
  - Microsoft Entra ID MFA (via SAML/OIDC ??" CyberArk Identity or PVWA federation)
  - Duo Security (via RADIUS)
  - RSA SecurID (via RADIUS)
  - CyberArk Identity (built-in MFA with Vault integration)
Best practice: enforce MFA via Conditional Access at the AD/Entra level
so all CyberArk logins (LDAP-authenticated) require MFA automatically.

Q5 ??" User offboarding process
Steps to fully revoke access:
1. Disable the user's AD account (if using LDAP integration, this
   immediately prevents login to CyberArk ??" most important step)
2. Remove the user from all CyberArk-related AD groups
3. PVWA ??' Users ??' find user ??' Deactivate (or Delete if local Vault user)
4. Review all Safes where the user was listed as a Safe Owner:
   PVWA ??' Safes ??' filter by owner = [user] ??' reassign ownership
5. Review Safe Members across all Safes for this user and remove their
   direct memberships (group removal in step 2 handles group-based access)
6. Check if user had any active PSM sessions ??' terminate if found
What happens to owned Safes: the Safe continues to exist. If the user
was the ONLY owner, the Safe becomes ownerless ??" assign a new owner
immediately. Never delete Safes without reviewing contents first.
"""
    },
]

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  ALL SCENARIOS ??" COMBINED POOL
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

ALL_CYBERARK_SCENARIOS = (
    DOMAIN1_SCENARIOS +
    DOMAIN2_SCENARIOS +
    DOMAIN3_SCENARIOS +
    DOMAIN4_SCENARIOS +
    DOMAIN5_SCENARIOS +
    DOMAIN6_SCENARIOS +
    DOMAIN7_SCENARIOS
)

# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
#  CORE GENERATOR FUNCTION
# ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?

def generate_cyberark_pbq(domain_filter=None, difficulty_filter=None):
    pool = ALL_CYBERARK_SCENARIOS
    if domain_filter:
        pool = [s for s in pool if s["domain"] == str(domain_filter)]
    if difficulty_filter and difficulty_filter != "beginner":
        filtered = [s for s in pool if s["difficulty"] == difficulty_filter]
        if filtered:
            pool = filtered
    template = random.choice(pool)
    scenario_text = template["scenario_template"]
    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace(f"{{{var_name}}}", chosen)
    domain_info = CYBERARK_EXAM["domains"][template["domain"]]
    return {
        "exam":            f"{CYBERARK_EXAM['name']} ({CYBERARK_EXAM['code']})",
        "id":              template["id"],
        "domain":          f"{template['domain']}. {domain_info['name']}",
        "sub_topic":       template["sub_topic"],
        "objective":       template["objective"],
        "difficulty":      template["difficulty"],
        "exam_objectives": ", ".join(template.get("exam_objectives", [])),
        "scenario":        scenario_text.strip(),
        "answers":         template.get("answers", "No answers available."),
    }


def get_weighted_cyberark_pbq():
    # Domain 6 (Session Management) has highest weight ~20%
    # Domains 1,3,4,5 are ~15% each
    # Domains 2,7 are ~10% each
    weights = [15, 10, 15, 15, 15, 20, 10]
    domain = random.choices(["1","2","3","4","5","6","7"], weights=weights, k=1)[0]
    return generate_cyberark_pbq(domain_filter=domain)


def display_cyberark_pbq(pbq: dict, student_mode: bool = False):
    separator = "=" * 70
    print(f"\n{separator}")
    print(f"  {pbq.get('exam', 'CyberArk Defender PAM-DEF')}")
    print(f"  Scenario ID : {pbq.get('id', 'N/A')}")
    print(f"  Domain      : {pbq.get('domain', 'N/A')}")
    print(f"  Sub-topic   : {pbq.get('sub_topic', 'N/A')}")
    print(f"  Objective   : {pbq.get('objective', 'N/A')}")
    print(f"  Difficulty  : {pbq.get('difficulty', 'N/A').upper()}")
    print(f"  Obj. Refs   : {pbq.get('exam_objectives', 'N/A')}")
    print(separator)
    print(pbq.get("scenario", "No scenario generated."))
    if not student_mode:
        answers = pbq.get("answers", "").strip()
        if answers:
            print(f"\n{separator}")
            print("  MODEL ANSWERS")
            print(separator)
            print(answers)
    print(f"\n{separator}\n")


if __name__ == "__main__":
    print("\nGIDEON - CyberArk Defender PAM-DEF Module Test")
    print("Generating 3 sample PBQs (weighted by domain)...\n")
    for i in range(3):
        pbq = get_weighted_cyberark_pbq()
        display_cyberark_pbq(pbq, student_mode=False)
        input("Press ENTER for next scenario...\n")


