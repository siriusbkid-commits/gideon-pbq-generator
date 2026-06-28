"""
GIDEON SC-300 Module
====================
Microsoft Identity and Access Administrator (SC-300)
Exam domains and weights (2025-01):
  1. Implement and Manage User Identities         20-25%
  2. Implement Authentication and Access Mgmt     25-30%
  3. Plan and Implement Workload Identities       20-25%
  4. Plan and Automate Identity Governance        20-25%
"""

import random

SC300_EXAM = {
    "code": "SC-300",
    "name": "Microsoft Identity and Access Administrator",
    "version": "2025-01",
    "domains": {
        "1": {"name": "Implement and Manage User Identities",         "weight": "20-25"},
        "2": {"name": "Implement Authentication and Access Management","weight": "25-30"},
        "3": {"name": "Plan and Implement Workload Identities",        "weight": "20-25"},
        "4": {"name": "Plan and Automate Identity Governance",         "weight": "20-25"},
    }
}

DOMAIN1_SCENARIOS = [
    {
        "id": "SC1-001",
        "domain": "1",
        "sub_topic": "Microsoft Entra Tenant Configuration",
        "objective": "1.1 - Configure and manage a Microsoft Entra tenant",
        "scenario_template": """
You are the Identity Administrator for {org_name}, a {org_size} organisation
operating in the {industry} sector. Your Microsoft Entra tenant has recently
been audited and the following issues were identified:

  - {num_global_admins} users hold the Global Administrator role
  - Administrative Units have not been configured despite {num_departments} departments
  - Custom Entra roles have not been created; all admins use built-in roles
  - Company branding is not configured (users see the default Microsoft login page)
  - Guest user access settings allow guests to enumerate the full directory

Questions:
1. {num_global_admins} Global Administrators violates the principle of least privilege.
   What is Microsoft's recommended maximum? Which built-in roles would you use
   instead for: resetting user passwords, managing licences, and reading audit logs?
2. Design an Administrative Unit structure for {num_departments} departments.
   What permissions would you delegate to each department's IT support staff and why?
3. You need a custom role that can manage only Conditional Access policies.
   Walk through the steps to create this role. What is the minimum permission required?
4. Configure Company branding for the tenant. List the elements you would customise
   and explain why this matters for a {industry} organisation.
5. Tighten the guest access settings to prevent directory enumeration.
   What specific settings would you change and where are they configured?
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Finance", "Tailwind Manufacturing", "Northwind Logistics"],
            "org_size": ["500-person", "1,200-person", "250-person", "3,000-person"],
            "industry": ["healthcare", "financial services", "manufacturing", "local government"],
            "num_global_admins": ["14", "22", "8", "31"],
            "num_departments": ["6", "10", "4", "15"],
        },
        "exam_objectives": ["1.1"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC1-001: Microsoft Entra Tenant Configuration

Q1 -- Global Administrator count and least-privilege roles
Microsoft recommends a maximum of 2-4 Global Administrators (typically
2 break-glass accounts + 1-2 active admins). Roles to use instead:
  - Reset user passwords -> Authentication Administrator (for non-admins)
    or Password Administrator
  - Manage licences -> Licence Administrator
  - Read audit logs -> Reports Reader or Security Reader
Never use Global Admin for tasks that scoped roles can perform.

Q2 -- Administrative Unit design
Create one AU per department. Delegate the Authentication Administrator
(scoped) role to each department's IT support staff, restricting their
actions to only that AU's members. Dynamic membership rules
(e.g. user.department -eq "Finance") keep AUs current automatically.
This enforces least privilege -- a helpdesk agent in Finance cannot
reset passwords for users in HR.

Q3 -- Custom role for Conditional Access only
Entra admin centre > Roles and administrators > New custom role.
Minimum permission required:
  microsoft.directory/conditionalAccessPolicies/allProperties/allTasks
Do NOT add any other permissions. Assign the role at tenant scope.
Test with a pilot user before broad assignment.

Q4 -- Company branding elements
Customise: sign-in page background image/colour, banner logo,
username hint text, sign-in page text, footer links (privacy/terms),
and SSPR link text. For regulated sectors (healthcare, finance) this
is critical for phishing resistance -- users recognise their org's
login page and are less likely to enter credentials on a spoofed page.
Path: Entra admin centre > User experiences > Company branding.

Q5 -- Guest access settings
Path: Entra admin centre > External Identities > External collaboration settings.
Changes:
  - Guest user access -> "Guest users have limited access to properties
    and memberships of directory objects" (or most restrictive option)
  - Who can invite guests -> Admins and users in the Guest Inviter role only
  - Collaboration restrictions -> Allow invitations only to specified domains
"""
    },
    {
        "id": "SC1-002",
        "domain": "1",
        "sub_topic": "Bulk Identity Operations and Licensing",
        "objective": "1.2 - Create, configure, and manage Microsoft Entra identities",
        "scenario_template": """
Your organisation has just acquired {acquired_company}, adding {num_new_users} new
employees who need Microsoft 365 accounts. You have {available_licences} Microsoft
365 {licence_type} licences available.

Requirements:
  - All new users must be in a dedicated group: "{new_group}"
  - {num_admins} of the new users are IT admins needing elevated access
  - All users need MFA enforced from day one
  - {num_contractors} are contractors who should NOT have access to SharePoint
  - Licence assignment must be automated based on department attribute

Questions:
1. Compare bulk creation via Entra admin centre CSV vs PowerShell vs Graph API.
   Which would you choose and why? Write the PowerShell command to create one user.
2. You have {available_licences} licences for {num_new_users} users.
   Configure a dynamic group rule that automatically assigns the {licence_type}
   licence to all full-time employees based on the employeeType attribute.
3. The {num_contractors} contractors must be blocked from SharePoint without
   revoking other M365 access. What is the cleanest way to achieve this?
4. Walk through creating a custom security attribute set to track department
   and contractor status. Who can assign values?
5. After bulk creation, how do you validate all accounts and licences are correct?
   List three verification methods.
""",
        "variables": {
            "acquired_company": ["Pacific Rim Solutions", "Southern Cross IT", "Alpine Data Services", "Bay Tech Group"],
            "num_new_users": ["85", "140", "220", "47"],
            "available_licences": ["100", "160", "250", "60"],
            "licence_type": ["E3", "E5", "Business Premium", "F3"],
            "new_group": ["ACQ-PacificRim-Users", "ACQ-Alpine-Users", "ACQ-BayTech-Users", "ACQ-SouthernCross-Users"],
            "num_admins": ["4", "6", "3", "8"],
            "num_contractors": ["12", "25", "8", "30"],
        },
        "exam_objectives": ["1.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC1-002: Bulk Identity Operations and Licensing

Q1 -- Bulk creation method comparison
  - Entra admin centre CSV upload: easiest for one-off ops, no coding required
  - PowerShell (Microsoft.Graph module): best for automation and transformation
  - Microsoft Graph API: best for long-term HR system integration
For a one-time acquisition, PowerShell is the pragmatic choice.
Example single user:
  New-MgUser -DisplayName "Jane Smith" -UserPrincipalName "jsmith@contoso.com" `
    -AccountEnabled -PasswordProfile @{Password="TempPass1!"; ForceChangePasswordNextSignIn=$true} `
    -UsageLocation "NZ" -Department "Finance" -EmployeeType "Employee"

Q2 -- Dynamic group + group-based licensing
Create dynamic security group rule: (user.employeeType -eq "Employee")
Assign licence to the group: Entra admin centre > Groups > [group] > Licences.
Select the licence plan and assign. Licence is automatically applied/removed
as users join or leave the group via attribute changes.

Q3 -- Blocking contractors from SharePoint only
Use group-based licensing with a contractor-specific licence profile.
Create a separate licence assignment for contractors that includes
Exchange Online and Teams but EXCLUDES the SharePoint Online plan.
Uncheck SharePoint Online in the licence assignment for the contractor group.
Do NOT remove their account -- just remove that specific service plan.

Q4 -- Custom security attributes
Entra admin centre > Custom security attributes > Add attribute set (e.g. "HR").
Add attributes: "Department" (string), "WorkerType" (string: Employee/Contractor).
Assign values: User profile > Custom security attributes > Edit.
Only users with the Attribute Assignment Administrator role can assign values.
Only users with Attribute Definition Administrator can create attribute sets.

Q5 -- Post-creation validation
1. Entra admin centre > Users > filter by createdDateTime -- verify count
2. PowerShell: Get-MgUser -Filter "createdDateTime ge [date]" | Measure-Object
3. Group-based licensing errors report: Groups > [licence group] > Licences --
   any users with assignment errors are flagged with the reason
"""
    },
    {
        "id": "SC1-003",
        "domain": "1",
        "sub_topic": "Hybrid Identity with Microsoft Entra Connect",
        "objective": "1.4 - Implement and manage hybrid identity",
        "scenario_template": """
{org_name} runs Active Directory on-premises with {num_ad_users} user accounts
across {num_domains} AD domains. They are migrating to Microsoft 365 and need
hybrid identity.

Current state:
  - AD Forest: {ad_forest}
  - Current auth method: {current_auth}
  - {legacy_app} uses AD FS for authentication
  - Users have separate on-prem and cloud passwords

Target state: Single sign-on with cloud-managed authentication.

Questions:
1. Compare Microsoft Entra Connect Sync vs Microsoft Entra Cloud Sync.
   Which would you recommend for this environment and why?
2. Walk through migrating {legacy_app} from AD FS to Microsoft Entra ID
   using {migration_method}. What pre-migration checks must you perform?
3. Configure Password Hash Synchronization as the primary auth method.
   What are the security implications of PHS vs PTA vs AD FS?
4. After enabling PHS, how do you implement Seamless SSO for domain-joined
   machines? List the GPO settings required.
5. What Microsoft Entra Connect Health alerts would you configure and
   what does each indicate?
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Ltd", "Northwind Bank", "Alpine Manufacturing"],
            "num_ad_users": ["2,400", "850", "5,000", "320"],
            "num_domains": ["2", "3", "1", "4"],
            "ad_forest": ["contoso.local", "fabrikam.internal", "northwind.corp", "alpine.lan"],
            "current_auth": ["AD FS 3.0", "AD FS 4.0 (Windows Server 2016)", "NTLM only"],
            "legacy_app": ["SAP HR Portal", "Oracle Finance System", "Legacy CRM", "SharePoint 2019"],
            "migration_method": ["SAML 2.0", "OpenID Connect", "WS-Federation"],
        },
        "exam_objectives": ["1.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC1-003: Hybrid Identity with Microsoft Entra Connect

Q1 -- Connect Sync vs Cloud Sync
Entra Connect Sync: full on-premises installation, supports complex
topologies, multi-forest, custom attribute mapping, writeback features.
Required for >100k objects or advanced transformation rules.
Entra Cloud Sync: lightweight provisioning agent (no full installation),
easier to deploy and maintain, supports most common single-forest scenarios.
Recommendation: for multiple AD domains with existing AD FS, use Connect Sync
for the migration due to the complex topology, then evaluate Cloud Sync post-stabilisation.

Q2 -- AD FS migration pre-migration checks
1. Run AD FS activity report in Entra Connect Health -- identify all relying
   party trusts and their last authentication date
2. Identify apps using custom AD FS claims rules that cannot be replicated in Entra ID
3. Test the target app in Entra ID using staged rollout before cutover
Migration steps: register app in Entra ID > configure SAML/OIDC SSO >
test with pilot group > cut over > decommission AD FS relying party trust.

Q3 -- PHS vs PTA vs AD FS
  - PHS: password hashes synced to cloud (encrypted hash of a hash).
    Enables leaked credential detection via ID Protection. Works during on-prem outage.
    Microsoft's recommended modern approach.
  - PTA: authentication validated on-prem in real time. No hash in cloud.
    Requires on-prem agent availability. No leaked credential detection.
  - AD FS: full on-prem auth, maximum control, maximum complexity and cost.
    Being phased out by Microsoft in favour of cloud auth.

Q4 -- Seamless SSO GPO settings
Deploy via Group Policy:
  Computer Configuration > Administrative Templates > Windows Components >
  Internet Explorer > Internet Control Panel > Security Page > Intranet Zone.
  Add: https://autologon.microsoftazuread-sso.com to Intranet zone sites.
  Also enable: "Allow updates to status bar via script" in Intranet zone.
Users on domain-joined machines will SSO without password prompts.

Q5 -- Connect Health alerts to configure
  - Password Hash Sync heartbeat failure (sync stopped running)
  - Sync errors (object-level failures blocking specific users)
  - Agent connectivity failure (Connect Health agent offline)
  - Duplicate attribute errors (UPN/ProxyAddress conflicts blocking sync)
  - AD FS token signing certificate expiry (if still using AD FS)
"""
    },
    {
        "id": "SC1-004",
        "domain": "1",
        "sub_topic": "External Identities and B2B Collaboration",
        "objective": "1.3 - Implement and manage identities for external users and tenants",
        "scenario_template": """
{org_name} works with {num_partners} external partner organisations and
{num_contractors} individual contractors who need access to specific M365 resources.

Current problems:
  - Partners are being added as internal users (consuming licences)
  - No cross-tenant access policies configured
  - External users can access ALL SharePoint sites
  - {partner_org} uses Google Workspace -- their users cannot currently authenticate
  - No lifecycle management for external accounts

Questions:
1. Configure External Collaboration settings to allow B2B invitations only
   from approved domains. List the specific settings and their location.
2. {partner_org} uses Google Workspace. Configure Google as a direct federation
   identity provider. What protocol is used and what information do you need?
3. Implement Cross-Tenant Access Settings between your tenant and {partner_org}
   to allow their users to access Teams without being MFA-prompted twice.
   Explain inbound vs outbound trust settings.
4. Design an automated lifecycle policy using Entra ID Governance that reviews
   external user access every {review_period} days and removes access if the
   reviewer does not respond within 14 days.
5. A contractor needs access to a single SharePoint site only. Walk through
   inviting them as a B2B guest and restricting their access. Is a licence required?
""",
        "variables": {
            "org_name": ["Contoso Health", "Tailwind Traders", "Northwind Bank", "Fabrikam Engineering"],
            "num_partners": ["8", "15", "3", "22"],
            "num_contractors": ["40", "120", "18", "65"],
            "partner_org": ["Pacific Rim Solutions", "Southern Labs", "Alpine Consulting", "Bay Data Co"],
            "review_period": ["30", "60", "90"],
        },
        "exam_objectives": ["1.3"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC1-004: External Identities and B2B Collaboration

Q1 -- External Collaboration settings
Path: Entra admin centre > External Identities > External collaboration settings.
  - Guest invite settings -> Only admins and users in the Guest Inviter role
  - Collaboration restrictions -> Allow invitations only to specified domains
    (add each approved partner domain to the allowlist)
  - Guest user access -> Restrict to own directory object properties only

Q2 -- Google federation
Google Workspace federation uses OpenID Connect (OIDC).
Path: External Identities > All identity providers > Google.
Information needed from partner's Google admin: their Google tenant domain
(e.g. partnerorg.com). No client ID/secret needed -- Google's standard
OIDC discovery endpoint is used automatically by Microsoft Entra ID.
Partner users sign in with their Google credentials directly.

Q3 -- Cross-Tenant Access Settings
Path: Entra admin centre > External Identities > Cross-tenant access settings.
Add partner tenant by tenant ID or domain.
  - Inbound settings: controls what THEIR users can do in YOUR tenant.
    Enable "Trust multifactor authentication from Microsoft Entra tenants"
    to prevent double MFA prompts.
  - Outbound settings: controls what YOUR users can do in THEIR tenant.

Q4 -- Guest lifecycle with Access Reviews
Path: Identity Governance > Access Reviews > New access review.
  - Scope: Guest users only
  - Recurrence: every chosen number of days
  - Reviewers: Sponsor (internal user who invited them)
  - Auto-apply results: Yes
  - If reviewers don't respond: Remove access
  - Notify sponsors before deadline via notification settings

Q5 -- Single SharePoint site guest access
Invite: Entra admin centre > Users > Invite external user.
Restrict access: SharePoint admin centre > Sites > [site] > Permissions > Share.
Do NOT add them to any M365 group or Teams channel.
Licence required: None. Guest users accessing SharePoint do not consume
a paid Entra ID licence (free tier allows up to 50,000 MAU free).
"""
    },
]

DOMAIN2_SCENARIOS = [
    {
        "id": "SC2-001",
        "domain": "2",
        "sub_topic": "Conditional Access Policy Design",
        "objective": "2.2 - Plan, implement, and manage Microsoft Entra Conditional Access",
        "scenario_template": """
You are designing Conditional Access policies for {org_name}.
Security requirements:

  1. All administrators must use MFA for every sign-in, regardless of location
  2. Standard users on compliant Entra-joined devices can access M365 without MFA
     when on the corporate network ({corp_ip_range})
  3. Standard users on non-compliant or personal devices must ALWAYS use MFA
  4. Access to {sensitive_app} requires MFA + compliant device with no exceptions
  5. Legacy authentication protocols must be blocked entirely
  6. The {service_account} service account must be excluded from all MFA policies

Questions:
1. Describe the report-only mode approach for requirement 1. What data do you
   review before switching the policy to "on"?
2. Design the Conditional Access policy for requirement 2. Specify assignments,
   access controls, and named location configuration for {corp_ip_range}.
3. Requirement 4 uses Authentication Context. Explain what this is and how it
   differs from a standard CA policy targeting an app directly.
4. What is the recommended discovery process before blocking legacy authentication?
   Name the specific workbook that shows legacy authentication usage.
5. The {service_account} must be excluded. What is the risk and what compensating
   control do you implement?
6. A user cannot sign in from home on their personal laptop. Walk through your
   CA troubleshooting process, naming the specific diagnostic tool.
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Finance", "Northwind Logistics", "Tailwind Manufacturing"],
            "corp_ip_range": ["203.0.113.0/24", "198.51.100.0/24", "192.0.2.0/24"],
            "sensitive_app": ["Finance ERP (SAP)", "HR Payroll System", "Patient Records (Epic)", "Treasury Management"],
            "service_account": ["svc-backup@contoso.com", "svc-reporting@fabrikam.com", "svc-integration@tailwind.com"],
        },
        "exam_objectives": ["2.2"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-001: Conditional Access Policy Design

Q1 -- Report-only mode
Create policy in Report-only mode. Monitor: Entra admin centre > Monitoring >
Sign-in logs > filter by CA policy name > review "Report-only" column.
Failure = would have been blocked. Check for: service accounts, legacy auth
clients, shared mailboxes, break-glass accounts being impacted.
Switch to "On" only when zero legitimate users show as "would fail."

Q2 -- Policy for compliant devices on corp network
  Assignments:
    Users: All users (exclude admins -- covered separately)
    Cloud apps: Office 365
    Conditions: Named location = corp IP range (trusted), Device = compliant
  Grant: Require device marked as compliant OR Hybrid Entra joined (OR logic)
  Named location: Entra > Security > CA > Named locations > IP ranges location.
  Mark as trusted location.

Q3 -- Authentication Context
Standard CA targets an entire app. Authentication Context targets a SPECIFIC
ACTION within an app (e.g. viewing payroll data within the HR app, not just
logging in). The app developer calls the auth context ID in their code when
the sensitive action is triggered. A separate CA policy enforces stricter
controls only when that context fires.
Path: Entra > Security > CA > Authentication context > Add.

Q4 -- Legacy authentication discovery
Run the "Sign-ins using legacy authentication" workbook:
Entra admin centre > Monitoring > Workbooks > Legacy Authentication.
Shows users, apps, and protocols (SMTP AUTH, POP3, IMAP) still using basic auth.
Remediate these BEFORE blocking -- otherwise legitimate services break.

Q5 -- Service account exclusion risk and compensating control
Risk: excluded accounts bypass all CA policies -- a compromised service account
gives an attacker unchecked access.
Compensating control: create a dedicated CA policy for the service account
that ONLY allows sign-in from specific named IP locations (server IPs),
blocking all other locations. Alert on any sign-in from outside those IPs.
Better long-term: replace service account with Managed Identity.

Q6 -- CA troubleshooting
1. Entra admin centre > Users > [user] > Sign-in logs
2. Find failed sign-in > click it > Conditional Access tab
3. Review which policies applied and what the outcome was
4. Use "What If" tool: Entra > Security > CA > What If
   Enter: user, app, IP, device state -> shows exactly which policies apply
5. Check for policy conflicts -- most restrictive policy wins
"""
    },
    {
        "id": "SC2-002",
        "domain": "2",
        "sub_topic": "Authentication Methods and MFA",
        "objective": "2.1 - Plan, implement, and manage Microsoft Entra user authentication",
        "scenario_template": """
{org_name} has {mfa_coverage}% of users enrolled in MFA using legacy per-user MFA.
The security team wants to modernise authentication.

Current issues:
  - Users are using SMS OTP as their only MFA method (phishing risk)
  - {num_exec} executives refuse to use the Authenticator app
  - {num_field} field workers do not have smartphones
  - SSPR is not enabled -- all resets go through the helpdesk
    ({monthly_resets} resets/month at ${reset_cost} each)
  - Windows Hello for Business is not deployed

Questions:
1. What is the key difference between per-user MFA and Authentication Methods
   policy? What must you disable to avoid conflicts?
2. Propose a phased migration plan to move users from SMS OTP to Microsoft
   Authenticator. How do you handle the {num_exec} executives who refuse?
3. The {num_field} field workers without smartphones need MFA. What Entra ID
   authentication methods do NOT require a smartphone?
4. Calculate the annual cost of not having SSPR. Configure SSPR with at least
   two authentication methods. Which methods suit a {industry} organisation?
5. What are the Windows Hello for Business prerequisites? What does WHfB replace
   and why is it phishing-resistant?
""",
        "variables": {
            "org_name": ["Contoso Health", "Pacific Finance Group", "Northwind Council", "Alpine Manufacturing"],
            "mfa_coverage": ["45", "62", "78", "30"],
            "num_exec": ["12", "8", "20", "5"],
            "num_field": ["80", "200", "35", "150"],
            "monthly_resets": ["120", "340", "60", "210"],
            "reset_cost": ["15", "25", "18", "30"],
            "industry": ["healthcare", "financial services", "local government", "manufacturing"],
        },
        "exam_objectives": ["2.1"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC2-002: Authentication Methods and MFA

Q1 -- Per-user MFA vs Authentication Methods policy
Per-user MFA (legacy): configured per-user in M365 admin centre, separate
from Conditional Access, limited method control.
Authentication Methods policy (modern): Entra > Security > Authentication methods.
Controls which methods are available tenant-wide, supports registration campaigns,
integrates fully with CA and ID Protection.
To avoid conflicts: disable legacy per-user MFA settings AND disable Security
defaults before enabling CA-based MFA.
Path to disable Security defaults: Entra > Overview > Properties > Manage security defaults.

Q2 -- Migration plan from SMS OTP to Authenticator
Phase 1 (weeks 1-2): Enable Authenticator in Authentication Methods policy.
  Enable registration campaign to nudge users at next sign-in.
Phase 2 (weeks 3-4): Set Authenticator as default method for enrolled users.
Phase 3 (week 5+): Disable SMS OTP in Authentication Methods policy.
For resistant executives: escalate to CISO, frame as SIM swap / phishing risk.
Offer FIDO2 security key as alternative. If still refused, document risk
acceptance and implement monitoring on their accounts.

Q3 -- MFA without a smartphone
Options in Microsoft Entra ID:
  - FIDO2 security key (YubiKey etc.) -- best for field workers
  - Temporary Access Pass (TAP) -- time-limited passcode for onboarding/recovery
  - Certificate-based authentication -- requires PKI infrastructure
  - Windows Hello for Business -- requires Windows device
Recommendation for field workers: FIDO2 security keys.
Path: Entra > Security > Authentication methods > FIDO2 security key > Enable.

Q4 -- SSPR cost and configuration
Annual cost = monthly resets x cost per reset x 12.
Configure: Entra > Security > Password reset > Self service password reset = All.
Require 2 authentication methods. Recommended methods for regulated sectors:
  - Microsoft Authenticator (primary)
  - Email to personal address (backup)
Avoid SMS as a method due to SIM swap risk.

Q5 -- Windows Hello for Business
Prerequisites: Windows 10/11 devices, Entra joined or Hybrid Entra joined,
Microsoft Entra ID P1 licence minimum, users must have completed MFA registration.
WHfB replaces: passwords for Windows sign-in and browser/app authentication.
Phishing resistance: uses asymmetric key cryptography. Private key never leaves
the device (protected by TPM). No password or OTP to intercept -- attacker
needs physical device access + PIN/biometric.
"""
    },
    {
        "id": "SC2-003",
        "domain": "2",
        "sub_topic": "Microsoft Entra ID Protection",
        "objective": "2.3 - Manage risk by using Microsoft Entra ID Protection",
        "scenario_template": """
Your Microsoft Entra ID Protection dashboard shows:

  - {num_risky_users} users flagged as HIGH risk
  - {num_risky_signins} risky sign-ins in the past 7 days
  - Top detections: {top_detection_1}, {top_detection_2}
  - {executive_account} (CFO) has a HIGH risk sign-in from {risky_location}
    at {risky_time} -- CFO confirmed they were in Auckland at that time
  - {num_mfa_not_registered} users have not completed MFA registration

Questions:
1. Explain the difference between User Risk and Sign-in Risk. What triggers each?
   How do risk levels affect policy decisions?
2. Configure a User Risk policy that requires password reset for HIGH risk users.
   Should this be a CA risk-based policy or the legacy ID Protection policy?
3. The CFO's sign-in is confirmed impossible travel. Walk through investigation
   and remediation. What does "Confirm compromised" vs "Dismiss user risk" do?
4. Configure an MFA Registration Campaign for the {num_mfa_not_registered}
   unregistered users. What happens to users who keep dismissing the prompt?
5. You want to monitor risky workload identities. What licence is required?
   What risk detections are available for workload identities vs users?
""",
        "variables": {
            "num_risky_users": ["23", "8", "47", "5"],
            "num_risky_signins": ["156", "42", "289", "17"],
            "top_detection_1": ["Unfamiliar sign-in properties", "Anonymous IP address", "Atypical travel"],
            "top_detection_2": ["Password spray", "Leaked credentials", "Malicious IP address"],
            "executive_account": ["cfo@contoso.com", "ceo@fabrikam.com", "cto@tailwind.com"],
            "risky_location": ["Bucharest, Romania", "Lagos, Nigeria", "Minsk, Belarus"],
            "risky_time": ["03:47 UTC", "02:15 UTC", "01:33 UTC"],
            "num_mfa_not_registered": ["34", "12", "89", "7"],
        },
        "exam_objectives": ["2.3"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC2-003: Microsoft Entra ID Protection

Q1 -- User Risk vs Sign-in Risk
User Risk: probability that an identity is compromised. Accumulates over time.
Triggered by: leaked credentials on dark web, unusual activity patterns,
admin confirmation of compromise.
Sign-in Risk: probability a specific authentication attempt is not from the
legitimate user. Per-sign-in. Triggered by: anonymous IP, atypical travel,
unfamiliar sign-in properties, malicious IP address.
Risk levels: Low -> log/monitor. Medium -> require MFA step-up.
High -> block or force password reset immediately.

Q2 -- Risk-based policy: CA vs legacy
Use Conditional Access risk-based policies (modern approach).
Legacy ID Protection policies (User/Sign-in risk policy tabs) are being
deprecated -- Microsoft recommends CA with risk conditions instead.
Configure: Entra > Security > CA > New policy > Conditions: User risk = High >
Grant: Require password change (requires SSPR to be enabled first).

Q3 -- Investigating impossible travel
1. Entra > Security > Identity Protection > Risky sign-ins
2. Find the CFO sign-in > review: IP, location, device, browser
3. CFO confirmed they were in Auckland -- select "Confirm compromised"
   (NOT "Dismiss" -- that clears the risk flag and loses the audit trail)
"Confirm compromised" -> sets user risk to High, triggers risk policy,
forces password reset, invalidates ALL active sessions.
"Dismiss user risk" -> clears risk flag (use ONLY for confirmed false positives).
4. Also: revoke sessions manually > investigate all activity since the foreign sign-in.

Q4 -- MFA Registration Campaign
Path: Entra > Security > Authentication methods > Registration campaign.
Settings: State = Enabled, Days allowed to snooze = 1-14 days.
Users who dismiss are prompted again after the snooze period.
After the configured number of snoozes they CANNOT complete sign-in
until they register -- they are forced to the registration experience.

Q5 -- Risky workload identities
Licence: Microsoft Entra ID P2 (Workload Identities Premium add-on
may be required separately for service principal risk detections).
Detections available for workload identities:
  - Suspicious sign-ins (unusual token request patterns)
  - Anomalous service principal activity
  - Leaked credentials (client secrets found in public repos via GitHub scanning)
NOT available for workload identities (unlike users):
  - Impossible travel, unfamiliar sign-in properties (no concept of location for SPs)
"""
    },
    {
        "id": "SC2-004",
        "domain": "2",
        "sub_topic": "Global Secure Access",
        "objective": "2.4 - Implement Global Secure Access",
        "scenario_template": """
{org_name} has {num_remote_users} remote workers accessing internal resources
via a legacy VPN ({vpn_product}). The security team wants Zero Trust network access.

Current pain points:
  - VPN grants access to the entire internal network (flat trust)
  - VPN client conflicts with endpoint security tools on {os_type} devices
  - Microsoft 365 traffic is hairpinned through the VPN (causing latency)
  - No visibility into which private resources remote users are accessing

Questions:
1. Explain the difference between Global Secure Access Private Access and
   Internet Access. Which replaces the legacy VPN?
2. Deploy the GSA client to {num_remote_users} remote workers on {os_type}.
   What are the prerequisites? How is the client deployed at scale?
3. Configure Private Access for {internal_app} running on {internal_server}
   on port {app_port}. Walk through the Connector, Application Segment,
   and access policy.
4. Configure Internet Access for Microsoft 365 to break out directly instead
   of hairpinning through the VPN. What specific traffic profile do you use?
5. How do you verify remote users are accessing {internal_app} through GSA
   and not the legacy VPN? What logs and dashboards are available?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Alpine Engineering", "Pacific Logistics"],
            "num_remote_users": ["180", "420", "75", "900"],
            "vpn_product": ["Cisco AnyConnect", "Palo Alto GlobalProtect", "Fortinet FortiClient", "Pulse Secure"],
            "os_type": ["Windows 11", "macOS Sequoia", "Windows 10 Enterprise"],
            "internal_app": ["HR Self-Service Portal", "Finance Reporting Dashboard", "Engineering Document Store", "Logistics Tracking System"],
            "internal_server": ["hrapp01.contoso.local", "finreport.fabrikam.internal", "docstore.alpine.lan"],
            "app_port": ["443", "8443", "8080", "4433"],
        },
        "exam_objectives": ["2.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-004: Global Secure Access

Q1 -- Private Access vs Internet Access
Private Access: Zero Trust Network Access (ZTNA) -- replaces VPN.
Provides access to specific private resources only, not the whole network.
Users connect to defined application segments -- zero lateral movement.
Internet Access: Secure Web Gateway for internet-bound traffic. Controls
what users can access online, plus Microsoft 365 traffic optimisation.
To replace the legacy VPN -> deploy Private Access.

Q2 -- GSA client deployment
Prerequisites: Microsoft Entra ID P1, device must be Entra joined or
Hybrid Entra joined, Global Secure Access enabled in Entra admin centre,
Private Network Connector deployed on-premises.
Deployment at scale for Windows: Microsoft Intune (Endpoint Manager).
Deploy the GSA client MSI as a Win32 app targeting the remote workers group.
For macOS: Intune macOS LOB app deployment.

Q3 -- Configuring Private Access
Step 1 -- Deploy Private Network Connector:
  Download from: Global Secure Access > Connect > Connectors.
  Install on on-premises Windows Server with line-of-sight to the app server.
  Only outbound HTTPS required -- no inbound firewall rules.
Step 2 -- Create Application Segment:
  Global Secure Access > Applications > Enterprise applications > New app.
  Add segment: FQDN or IP of app server + port.
Step 3 -- Assign users/groups to the application.
Step 4 -- Create CA policy targeting the GSA app to enforce MFA + compliant device.

Q4 -- Microsoft 365 traffic profile
Global Secure Access > Traffic forwarding > Microsoft 365 access profile > Enable.
This uses Microsoft's optimised network paths, bypassing the VPN hairpin.
Profile automatically includes correct M365 endpoints (Exchange, SharePoint, Teams).
No manual endpoint configuration required.

Q5 -- Verifying GSA usage
Global Secure Access > Monitor > Traffic logs -- filter by app name, user, connector.
Dashboard: Global Secure Access > Dashboard -- connected users, top apps, connector health.
Cross-check: VPN gateway logs for the same user should show a drop in traffic
volume after the GSA client is deployed and active.
"""
    },
]

DOMAIN3_SCENARIOS = [
    {
        "id": "SC3-001",
        "domain": "3",
        "sub_topic": "Managed Identities and Service Principals",
        "objective": "3.1 - Plan and implement identities for applications and Azure workloads",
        "scenario_template": """
Your development team has deployed {num_apps} Azure workloads that currently
authenticate using {current_auth_method}. A security review flagged this as critical.

Affected workloads:
  - {app1}: Azure Function writing to Azure Blob Storage
  - {app2}: Azure VM running batch jobs querying Azure SQL Database
  - {app3}: AKS pod accessing Key Vault secrets
  - {app4}: Logic App sending emails via Microsoft Graph API

Questions:
1. Explain System-Assigned vs User-Assigned Managed Identity. For each workload
   above, recommend which type is more appropriate and justify your choice.
2. Enable a System-Assigned Managed Identity on {app1} and grant it minimum
   RBAC access to write to Azure Blob Storage. What is the role name and scope?
3. {app3} runs on AKS and needs Key Vault access. Configure Workload Identity
   Federation for AKS. How does this differ from assigning MI to the node pool?
4. {app4} needs to call Microsoft Graph to send emails. Create an App Registration.
   What API permission is required? Delegated or Application, and why?
5. After migrating all workloads away from {current_auth_method}, how do you
   verify no credentials remain hardcoded? Name a specific Azure tool.
""",
        "variables": {
            "num_apps": ["4", "7", "12", "3"],
            "current_auth_method": [
                "hardcoded service account passwords in app config files",
                "shared client secrets stored in Azure App Configuration",
                "a single service principal with Owner rights on the subscription",
            ],
            "app1": ["InvoiceProcessor-Func", "ReportGenerator-Func", "DataIngestion-Func"],
            "app2": ["NightlyBatch-VM", "ETL-Pipeline-VM", "ReportRunner-VM"],
            "app3": ["PaymentService-AKS", "AuthService-AKS", "DataAPI-AKS"],
            "app4": ["NotificationSender-LA", "AlertDispatcher-LA", "ApprovalWorkflow-LA"],
        },
        "exam_objectives": ["3.1"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC3-001: Managed Identities and Service Principals

Q1 -- System-Assigned vs User-Assigned
System-Assigned: tied to one resource, deleted when resource is deleted.
Best for single-resource workloads.
User-Assigned: created independently, assignable to multiple resources,
persists independently of any resource.
Recommendations:
  - Azure Function (app1) -> System-Assigned (single resource, simple)
  - Azure VM batch job (app2) -> System-Assigned (single VM)
  - AKS pod (app3) -> User-Assigned (pods are ephemeral; need persistent identity)
  - Logic App (app4) -> System-Assigned (single resource)

Q2 -- Enable MI on Azure Function + RBAC
Azure portal > Function App > [app] > Identity > System assigned > On > Save.
Note the Object ID generated.
Assign RBAC: Storage Account > Access Control (IAM) > Add role assignment.
Role: "Storage Blob Data Contributor" (minimum for write access).
Assign to: Managed identity > select the Function App.
Do NOT use Owner or Contributor -- violates least privilege.

Q3 -- AKS Workload Identity Federation
WIF uses the AKS OIDC issuer URL to federate with Entra ID. The pod
presents a Kubernetes service account token which Entra ID trusts and
exchanges for an Entra access token.
vs node pool MI: assigning MI to node pool gives ALL pods on that node
the same identity -- violates least privilege. WIF scopes identity to
individual pods/service accounts.
Setup: enable OIDC issuer on AKS cluster > create User-Assigned MI >
create federated credential using AKS OIDC issuer URL +
Kubernetes namespace + service account name.

Q4 -- App Registration for Microsoft Graph (Logic App)
Create App Registration: Entra > App registrations > New registration.
API permissions > Microsoft Graph > Application permissions (NOT delegated
-- no signed-in user exists for a Logic App running unattended):
Permission: Mail.Send
Click "Grant admin consent" -- Application permissions always require admin consent.
Delegated = acts as a signed-in user. Application = acts as itself (daemon/service).

Q5 -- Detecting exposed credentials
Microsoft Defender for Cloud: "Secrets should not be hardcoded" recommendation
via Defender for DevOps / GitHub Advanced Security integration.
Microsoft Entra ID Protection: detects leaked credentials (client secrets
found in public repositories via GitHub secret scanning partnership).
Azure App Service / Function App: Key Vault Reference scanning flags
plaintext connection strings in app configuration.
"""
    },
    {
        "id": "SC3-002",
        "domain": "3",
        "sub_topic": "Enterprise Application Integration",
        "objective": "3.2 - Plan, implement, and monitor the integration of enterprise applications",
        "scenario_template": """
{org_name} needs to integrate {num_saas_apps} new SaaS applications into
Microsoft Entra ID for SSO and automated provisioning.

Applications to integrate:
  - {saas_app1}: Supports SAML 2.0 SSO and SCIM provisioning
  - {saas_app2}: Supports OpenID Connect only, no SCIM
  - {saas_app3}: Legacy on-premises web app (no federation support)
  - {saas_app4}: Available in the Entra application gallery

The security team also found {num_shadow_apps} shadow IT applications
discovered through Defender for Cloud Apps.

Questions:
1. For {saas_app1}, configure SAML 2.0 SSO. What four pieces of information
   do you need from the vendor? What do you provide back from Entra ID?
2. {saas_app2} supports OIDC but not SCIM. How do you handle user provisioning?
   What Entra feature can provide automated provisioning for gallery apps?
3. {saas_app3} is an on-premises app with no federation support. Configure
   Microsoft Entra Application Proxy. What must be installed on-premises?
   What authentication methods does App Proxy support?
4. {saas_app4} is in the Entra gallery. Walk through adding it and configuring
   SCIM provisioning. What does "on-demand provisioning" let you do?
5. A user sees {saas_app1} in My Apps but gets an error when clicking it.
   Walk through your SSO troubleshooting process. Name the specific tool.
""",
        "variables": {
            "org_name": ["Contoso", "Fabrikam", "Tailwind", "Northwind"],
            "num_saas_apps": ["4", "8", "12", "6"],
            "saas_app1": ["Salesforce", "ServiceNow", "Workday", "Zendesk"],
            "saas_app2": ["Slack", "Zoom", "DocuSign", "Dropbox Business"],
            "saas_app3": ["Legacy Timesheet System", "On-prem CRM", "Internal Wiki", "HR Self-Service (IIS)"],
            "saas_app4": ["AWS IAM Identity Center", "GitHub Enterprise", "Atlassian Cloud", "Box"],
            "num_shadow_apps": ["23", "47", "11", "68"],
        },
        "exam_objectives": ["3.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC3-002: Enterprise Application Integration

Q1 -- SAML 2.0 SSO configuration
Information needed FROM the vendor (Service Provider):
  1. SP Entity ID (Audience URI)
  2. ACS URL (Assertion Consumer Service URL)
  3. Required claims/attributes (email, surname, given name, roles)
  4. Signature requirements (SHA-256?)
Information provided TO the vendor FROM Entra ID:
  1. Entra Login URL (SAML SSO URL)
  2. Entra Identifier (Entity ID)
  3. Federation Metadata XML URL (or certificate download)
  4. Logout URL

Q2 -- Provisioning without SCIM
For gallery apps: check if a proprietary Entra provisioning connector exists
(many gallery apps have Entra-built provisioning even without published SCIM).
Path: Enterprise apps > [app] > Provisioning > Provisioning mode: Automatic.
If no connector exists: manual provisioning -- assign users in Entra, create
matching accounts manually in the target app.
On-demand provisioning: Provisioning > Provision on demand -- test provisioning
a single user before enabling the full automated cycle.

Q3 -- Microsoft Entra Application Proxy
On-premises requirement: Application Proxy Connector installed on a
Windows Server inside the network. Only outbound HTTPS required --
no inbound firewall rules needed.
Pre-authentication options:
  - Microsoft Entra ID (recommended): users auth to Entra before request
    reaches the on-prem app. Enforces CA policies.
  - Passthrough: no pre-auth (less secure).
SSO methods: Kerberos Constrained Delegation (KCD) for Windows-auth apps,
header-based SSO, SAML-based SSO, password-based SSO.

Q4 -- Gallery app SCIM provisioning
Add from gallery: Entra > Enterprise apps > New application > search.
Provisioning > Provisioning mode: Automatic.
Enter SCIM endpoint URL and secret token from vendor.
Scope: "Sync only assigned users and groups" (recommended over sync all).
On-demand provisioning: Provisioning > Provision on demand > enter a specific
user to test provisioning before enabling the full automated cycle.

Q5 -- SSO troubleshooting
Tool: use the "Test" button in Enterprise apps > [app] > Single sign-on.
The SAML-based SSO test experience shows the raw SAML response and
highlights claim mismatches.
Common causes:
  - UPN in Entra doesn't match NameID expected by the app
  - Required claim not mapped (e.g. app expects "role" claim)
  - Certificate mismatch (app has old signing cert cached)
  - Account not provisioned in the target app
"""
    },
    {
        "id": "SC3-003",
        "domain": "3",
        "sub_topic": "App Registrations and API Permissions",
        "objective": "3.3 - Plan and implement app registrations",
        "scenario_template": """
Your development team is building {app_name}, a {app_type} that needs to:
  - Authenticate users via Microsoft Entra ID (OIDC)
  - Read the signed-in user's profile from Microsoft Graph
  - Access {backend_api} on behalf of the signed-in user
  - Run a nightly background job reading all users in the tenant
    (no signed-in user context)

Questions:
1. This application requires two separate app registrations. Explain why.
   What is the key difference in the OAuth 2.0 flow each uses?
2. Configure the Redirect URI for the frontend {app_type} registration.
   What platform type do you select and what format does the URI take?
3. The background job needs to read all users with no signed-in user.
   What Graph permission is required? Delegated or Application, and why?
   Who must grant admin consent?
4. Configure the {backend_api} app registration to expose an API.
   Walk through: Application ID URI, adding scope "{scope_name}", and
   granting the frontend app permission to that scope.
5. The client secret for the background job expires in {secret_expiry} days.
   What is the recommended production alternative to client secrets?
""",
        "variables": {
            "app_name": ["ContosoBudgetTracker", "NorthwindInventoryPortal", "FabrikamLeaveManager", "TailwindProjectHub"],
            "app_type": ["Single-Page Application (SPA)", "Web Application (.NET)", "Mobile App (iOS)", "Web Application (Python/Django)"],
            "backend_api": ["ContosoBudgetAPI", "NorthwindInventoryAPI", "FabrikamHRAPI", "TailwindProjectAPI"],
            "scope_name": ["Budget.Read", "Inventory.ReadWrite", "Leave.Submit", "Projects.Manage"],
            "secret_expiry": ["14", "30", "7", "45"],
        },
        "exam_objectives": ["3.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC3-003: App Registrations and API Permissions

Q1 -- Why two app registrations
Frontend (interactive): uses Authorization Code Flow with PKCE -- user signs in,
gets delegated token representing the user. Delegated permissions only.
Background job (daemon): uses Client Credentials Flow -- no user, app acts
as itself. Requires Application permissions and admin consent.
These flows and permission models are incompatible in a single registration.
Separate registrations enforce least privilege -- the frontend cannot use
Application permissions and the daemon cannot impersonate users.

Q2 -- Redirect URI by app type
Single-Page Application (SPA):
  Platform: Single-page application
  URI format: https://app.contoso.com/auth/callback
  SPA uses Authorization Code + PKCE (no client secret -- cannot be kept
  secure in browser-side JavaScript).
Web Application (.NET): Platform = Web, URI = https://app/signin-oidc.
Mobile (iOS): Platform = Mobile and desktop, URI = msauth.[bundle-id]://auth.

Q3 -- Background job Graph permission
Permission: User.Read.All
Type: Application permission (no signed-in user context).
Admin consent: required. Only Global Administrator or Privileged Role
Administrator can grant admin consent for Application permissions.
Reason: Application permissions grant app-level access to ALL tenant data
in that scope -- cannot be delegated to end users.
Path: App registration > API permissions > Grant admin consent for [tenant].

Q4 -- Expose an API (backend registration)
App registration for backend API:
  Expose an API > Set Application ID URI (e.g. api://[client-id]).
  Add a scope:
    Scope name: Budget.Read
    Who can consent: Admins and users
    Admin/User consent display names: set appropriately.
Grant frontend app access to this scope:
  Frontend app registration > API permissions > Add permission >
  My APIs > [backend API] > Delegated permissions > Budget.Read.

Q5 -- Alternative to client secrets
Recommended: Certificate credentials (X.509 certificate).
App holds the private key; Entra ID validates the public key.
Certificates cannot be copied as easily as secrets and integrate with
Azure Key Vault for automated rotation.
Best for Azure workloads: Managed Identity -- no credential at all to manage.
For SPA: no client secret is used by design (PKCE flow).
Path to upload certificate: App registration > Certificates and secrets >
Certificates tab > Upload certificate (.cer or .pem).
"""
    },
]

DOMAIN4_SCENARIOS = [
    {
        "id": "SC4-001",
        "domain": "4",
        "sub_topic": "Privileged Identity Management (PIM)",
        "objective": "4.3 - Plan and implement privileged access",
        "scenario_template": """
{org_name} has just enabled Microsoft Entra PIM for the first time.
Current state:

  - {num_permanent_admins} users have PERMANENT Global Administrator assignment
  - {num_eligible} users need occasional admin access (currently permanent)
  - {risky_role} assigned to {num_risky} users with no approval required
  - Break-glass accounts: {break_glass_status}
  - PIM for Groups: not configured
  - Azure resource roles in PIM: not configured

Questions:
1. Convert {num_permanent_admins} permanent Global Admins to eligible assignments.
   What activation settings would you configure: duration, MFA, justification, approval?
2. Configure PIM settings for {risky_role}: require approval from {approver_group},
   maximum activation {max_activation} hours, require MFA and justification,
   send notifications to the security team. Walk through each setting location.
3. {break_glass_status}. Create two break-glass accounts per Microsoft recommendations.
   What makes them different from standard admin accounts? How do you monitor them?
4. A team of {num_devops} DevOps engineers needs Owner access to the Production
   subscription for deployment windows only. Configure this using PIM for Azure
   Resources. How does this differ from PIM for Entra roles?
5. Configure PIM for Groups so members of "{pim_group}" activate membership
   before gaining access to associated resources. What licence is required?
6. Generate a PIM audit report for the past 30 days showing all role activations.
   How do you export this for a compliance audit?
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Finance", "Northwind Bank", "Pacific Gov"],
            "num_permanent_admins": ["8", "14", "5", "22"],
            "num_eligible": ["15", "30", "8", "45"],
            "risky_role": ["Privileged Role Administrator", "Exchange Administrator", "SharePoint Administrator", "Security Administrator"],
            "num_risky": ["6", "3", "10", "4"],
            "break_glass_status": [
                "no break-glass accounts exist",
                "one break-glass account exists but is not monitored",
                "break-glass accounts exist but use the same MFA method as regular admins",
            ],
            "approver_group": ["Identity-Admins", "Security-Team", "IT-Leadership", "IAM-Approvers"],
            "max_activation": ["2", "4", "8"],
            "num_devops": ["6", "12", "4", "20"],
            "pim_group": ["Prod-Deployment-Team", "DR-Response-Team", "Security-Ops", "CloudOps-Admins"],
        },
        "exam_objectives": ["4.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-001: Privileged Identity Management (PIM)

Q1 -- Converting permanent to eligible assignments
Path: Entra admin centre > Identity Governance > PIM > Microsoft Entra roles >
Assignments > [Global Administrator].
For each admin: Remove permanent active assignment > Add eligible assignment.
Activation settings (PIM role settings for Global Administrator):
  - Maximum activation duration: 4-8 hours (not 24 -- limits exposure window)
  - Require MFA on activation: Yes (always for Global Admin)
  - Require justification: Yes (creates audit trail for every activation)
  - Require approval: Yes (Global Admin is too powerful to self-activate)
  - Approvers: 2-3 senior security team members

Q2 -- PIM settings for high-risk role
Path: Entra admin centre > PIM > Microsoft Entra roles > [role name] > Settings > Edit.
  - Activation maximum duration: set to chosen hours
  - On activation, require: MFA, Justification, Approval
  - Approval: add approver group members
  - Notification: "Alert admins when eligible members activate" -> add security team email
  - Assignment: prevent permanent active assignments (eligible only)
All settings are on the "Settings" tab for the specific role in PIM.

Q3 -- Break-glass accounts
Microsoft recommendations:
  - Create 2 accounts (so one is available if the other is locked)
  - Use .onmicrosoft.com UPN (not federated -- works even if federation/MFA fails)
  - Do NOT require MFA via Conditional Access (exclude from ALL CA policies)
  - Use FIDO2 hardware key or very long random password stored in physical safe
  - Assign Global Administrator PERMANENTLY (not eligible -- must work if PIM is down)
  - Monitor: create alert in Sentinel/Log Analytics -- ANY sign-in from these
    accounts triggers immediate security team notification

Q4 -- PIM for Azure Resources vs Entra roles
PIM for Entra roles: manages directory roles (Global Admin, User Admin, etc.)
PIM for Azure Resources: manages Azure RBAC roles (Owner, Contributor, etc.)
on subscriptions, resource groups, or individual resources.
Path: PIM > Azure resources > [Production subscription] > Roles > Owner >
Add eligible assignment > select DevOps group members > set time-bound duration.

Q5 -- PIM for Groups
Licence: Microsoft Entra ID P2.
Path: PIM > Groups > Discover groups > select security group > Enable PIM.
Members now activate their group membership before the group (and its
associated resource access/app role assignments) takes effect.
Use case: group is assigned to an app role or used in a CA policy --
PIM for Groups gates that access behind activation.

Q6 -- PIM audit report
Path: PIM > Microsoft Entra roles > Audit history.
Filter: Date range = last 30 days, Activity = "Role activated."
Export: Download CSV from the audit history view.
Report shows: who activated, which role, when, duration, justification provided,
whether approval was required and granted. Suitable for compliance audit submission.
"""
    },
    {
        "id": "SC4-002",
        "domain": "4",
        "sub_topic": "Access Reviews",
        "objective": "4.2 - Plan, implement, and manage access reviews in Microsoft Entra",
        "scenario_template": """
A compliance audit at {org_name} found these access control weaknesses:

  - {num_stale_users} accounts not signed in for 90+ days still retain full access
  - {num_privileged} privileged role members have never had their access reviewed
  - {num_guests} guest accounts in the tenant for over {guest_age} months with no review
  - {sensitive_group} grants access to {sensitive_data} -- not reviewed in {review_gap} months
  - Terminated employees: {term_employee_status}

Questions:
1. Create a recurring Access Review for {sensitive_group} every {review_frequency} days.
   Who should be the reviewer -- group owner, the users themselves, or selected reviewers?
   Justify for a {sensitive_data} scenario.
2. Configure an Access Review for the {num_privileged} privileged role members.
   What is different about reviewing privileged roles vs group membership?
3. What happens when a reviewer does NOT respond by the deadline? Configure the
   appropriate "no response" setting for {sensitive_group} and explain your choice.
4. Configure an Access Review targeting guest users only with auto-removal.
   What setting removes guests automatically if their access is denied?
5. {term_employee_status}. Design a Lifecycle Workflow that runs when
   employeeLeaveDateTime is set. What trigger type and tasks would you configure?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Alpine Council", "Pacific Insurance"],
            "num_stale_users": ["67", "143", "28", "312"],
            "num_privileged": ["18", "7", "34", "12"],
            "num_guests": ["89", "240", "34", "178"],
            "guest_age": ["6", "12", "18", "24"],
            "sensitive_group": ["Finance-FullAccess", "PatientRecords-Admins", "PayrollSystem-Users", "BoardDocuments-Access"],
            "sensitive_data": ["financial records", "patient health information", "payroll data", "board-level documents"],
            "review_gap": ["18", "24", "12", "36"],
            "term_employee_status": [
                "terminated employees are being manually offboarded -- 3 recently missed",
                "there is no automated offboarding process in place",
                "HR updates AD but Entra ID sync takes up to 24 hours",
            ],
            "review_frequency": ["30", "60", "90"],
        },
        "exam_objectives": ["4.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC4-002: Access Reviews

Q1 -- Access Review for sensitive group
Path: Entra admin centre > Identity Governance > Access Reviews > New access review.
  - Review type: Teams + Groups > select the sensitive group
  - Recurrence: chosen frequency (e.g. every 90 days)
  - Reviewers: Selected reviewers -- choose the data owner or line manager
Do NOT use self-review for sensitive data: users have a conflict of interest
reviewing their own access to payroll, patient records, or financial data.
For sensitive data always use a named manager, data owner, or security reviewer.

Q2 -- Privileged role access review
Path: Access Reviews > New access review > Microsoft Entra roles.
Key differences from group review:
  - Scope can target only active or only eligible PIM assignments (or both)
  - Results can auto-remove eligible assignments if denied (PIM integration)
  - Review scope = specific privileged roles, not group membership
  - Recommended reviewer: a senior security team member, not the role holders themselves

Q3 -- No-response setting
Path: Access Reviews > [review] > Settings > "If reviewers don't respond."
For a sensitive group: set to "Remove access."
Rationale: if a reviewer cannot confirm that someone still needs access to
sensitive data, access should default to denied (least privilege principle).
Never use "Approve access" as a no-response default for sensitive resources.

Q4 -- Guest-specific review with auto-removal
Configure: scope = Guest users only.
Enable: Auto apply results to resource = Yes.
Enable: If reviewer doesn't respond = Remove access.
Enable: Action on denied guest users = Remove user's membership from the group
AND disable sign-in (prevents lingering directory presence).

Q5 -- Lifecycle Workflow for offboarding
Path: Entra admin centre > Identity Governance > Lifecycle Workflows > New workflow.
  - Trigger type: "Employee leave" (triggered when employeeLeaveDateTime is set)
  - Tasks:
    1. Disable user account
    2. Remove user from all groups
    3. Remove user from all Teams
    4. Send email notification to manager
    5. (Optional) Remove user's app role assignments
  - Schedule: real-time trigger or daily sweep
The workflow fires when the HR system writes the employeeLeaveDateTime attribute
via writeback or direct Entra attribute update.
"""
    },
    {
        "id": "SC4-003",
        "domain": "4",
        "sub_topic": "Entitlement Management and Access Packages",
        "objective": "4.1 - Plan and implement entitlement management in Microsoft Entra",
        "scenario_template": """
{org_name} has {num_apps} applications and {num_groups} security groups controlling
access. Currently access requests are managed via email to the IT helpdesk --
causing delays and no audit trail.

Access requirements to automate:
  - New {department} employees need: {dept_resources}
  - External contractors need time-limited access to {contractor_resources}
    for a maximum of {contractor_duration} days
  - {partner_org} partners need access to a shared SharePoint site and Teams channel
  - All users must accept {tou_name} Terms of Use before accessing {sensitive_app}

Questions:
1. Design the Catalog and Access Package structure for the {department} department.
   What is the difference between a Catalog and an Access Package?
   Who should be the Catalog owner vs Access Package manager?
2. Configure the Access Package for new {department} employees with:
   - Manager approval workflow
   - Auto-assignment when a user joins the {department} department
   - Access expiry after {expiry_days} days requiring renewal
3. Configure an Access Package for {partner_org} contractors with time-limited
   access for {contractor_duration} days. What must be configured under
   "Connected organizations" first?
4. Implement the {tou_name} Terms of Use requirement for {sensitive_app}.
   What format must the document be in? How do you enforce it?
5. After 6 months, how do you report on who has access via Entitlement Management?
   What happens to access when an Access Package assignment expires and
   the user does not renew?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Pacific Engineering", "Alpine Council"],
            "num_apps": ["15", "28", "8", "42"],
            "num_groups": ["34", "67", "19", "120"],
            "department": ["Finance", "Clinical", "Engineering", "Legal"],
            "dept_resources": [
                "Finance ERP, Budget SharePoint site, Finance-Users group",
                "Patient Records app, Clinical Teams channel, EMR-Access group",
                "Azure DevOps, GitHub Enterprise, Engineering-Devs group",
                "Legal DMS, Contracts SharePoint, Legal-Staff group",
            ],
            "contractor_resources": [
                "Project SharePoint site and Teams channel",
                "Dev environment access and code repository",
                "Finance reporting dashboard (read-only)",
                "Document management system (read-only)",
            ],
            "contractor_duration": ["30", "60", "90"],
            "partner_org": ["Pacific Rim Consulting", "Southern Cross Partners", "Alpine Advisory", "Bay Group"],
            "tou_name": ["Data Handling Policy v2", "Acceptable Use Policy 2025", "Information Security Policy", "Patient Data Agreement"],
            "sensitive_app": ["Finance ERP", "Patient Records System", "HR Payroll Portal", "Legal Case Management"],
            "expiry_days": ["90", "180", "365"],
        },
        "exam_objectives": ["4.1"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC4-003: Entitlement Management and Access Packages

Q1 -- Catalog vs Access Package
Catalog: a container grouping related resources (apps, groups, SharePoint sites)
and defining who can manage them. Department-level container.
Access Package: a bundle of specific resources within a catalog that users
can request or be auto-assigned. Think of it as a role or job profile.
Catalog owner: department head or IT lead -- manages what resources are in the catalog.
Access Package manager: IT admin or HR -- manages approval workflows and policies.
Separation of duties: catalog owner ? access package manager.

Q2 -- Access Package for new employees with auto-assignment
Path: Identity Governance > Entitlement Management > Access packages > New.
Resources tab: add required groups, apps, SharePoint sites.
Requests tab -- add two policies:
  Policy 1 (auto-assignment): "Automatic assignment" rule:
    (user.department -eq "Finance") -- users matching this are auto-assigned.
    No approval required for auto-assignment.
  Policy 2 (self-service request): require manager approval for manual requests.
Lifecycle tab: Expiration = after chosen days, require renewal = Yes.

Q3 -- External Access Package (Connected Organizations)
Prerequisite: Identity Governance > Entitlement Management > Connected organizations >
New connected organization. Add partner org by domain or tenant ID. State = Configured.
Then in Access Package > Requests tab: add policy for "Users not in your directory"
> select the connected organization.
Set approval: require sponsor or admin approval.
Set expiration: time-limit to contractor duration days (hard expiry, no renewal).

Q4 -- Terms of Use enforcement
ToU document must be in PDF format.
Enforcement: via Conditional Access (not directly within the Access Package).
Create ToU: Entra admin centre > Identity Governance > Terms of use > New terms.
Upload PDF, configure language settings, require expansion before acceptance.
Create CA policy: target the sensitive app > Grant: Require terms of use.
The Access Package grants access; CA enforces ToU acceptance at sign-in time.

Q5 -- Reporting and expiry behaviour
Report: Identity Governance > Entitlement Management > Reports >
"Access package assignments" -- shows all current assignments, expiry dates, policies.
Also: "Requests" report (all requests, approvals, denials, cancellations).
When assignment expires without renewal:
  - Auto-apply removes user from all resources in the package
  - User loses access to all included groups, apps, and SharePoint sites immediately
  - User receives expiry notification email if configured
  - Assignment record retained in audit logs for compliance
"""
    },
    {
        "id": "SC4-004",
        "domain": "4",
        "sub_topic": "Identity Monitoring, Logs, and Reporting",
        "objective": "4.4 - Monitor identity activity by using logs, workbooks, and reports",
        "scenario_template": """
{org_name}'s Entra ID logs are only retained for the default period
({default_retention} days for sign-in logs). A security incident 45 days ago
cannot be fully investigated because logs have been purged.

Current monitoring gaps:
  - No diagnostic settings configured
  - No Azure Monitor Workbooks deployed
  - No KQL queries in Log Analytics for alerting
  - Identity Secure Score: {secure_score}/100
  - {num_secure_score_actions} high-impact improvement actions not implemented

Questions:
1. Configure Diagnostic Settings to export Entra ID logs to {log_destination}.
   What log categories should you export? What is the difference in cost and
   capability between Log Analytics vs Storage Account?
2. Write a KQL query that detects a user signing in from more than {geo_count}
   different countries within a 24-hour period.
3. Which built-in Entra Workbook would you use to:
   a) Identify users signing in with legacy authentication?
   b) Review Conditional Access policy impact before enforcement?
   c) Monitor risky sign-ins over time?
4. Your Identity Secure Score is {secure_score}/100. Describe how to implement
   these top improvement actions:
   - "Require MFA for administrative roles"
   - "Enable self-service password reset"
   - "Do not expire passwords"
5. A user account is suspected of compromise. Using only the Entra admin centre,
   walk through the investigation using sign-in and audit logs.
   What specific filters and fields would you examine?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Pacific Council", "Alpine Manufacturing"],
            "default_retention": ["7", "30"],
            "log_destination": [
                "a Log Analytics Workspace (Microsoft Sentinel)",
                "an Azure Storage Account for long-term archival",
                "Azure Event Hubs for SIEM integration (Splunk)",
            ],
            "secure_score": ["34", "52", "71", "28"],
            "num_secure_score_actions": ["5", "3", "7", "4"],
            "geo_count": ["3", "5", "2"],
        },
        "exam_objectives": ["4.4"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC4-004: Identity Monitoring, Logs, and Reporting

Q1 -- Diagnostic Settings
Path: Entra admin centre > Monitoring > Diagnostic settings > Add diagnostic setting.
Log categories to export:
  - SignInLogs (interactive user sign-ins)
  - NonInteractiveUserSignInLogs (service/app sign-ins)
  - ServicePrincipalSignInLogs (workload identity sign-ins)
  - AuditLogs (directory changes: user creation, role assignments, etc.)
  - RiskyUsers and UserRiskEvents (ID Protection events)
  - ManagedIdentitySignInLogs
Log Analytics vs Storage Account:
  - Log Analytics: query with KQL in real time, integrate with Sentinel,
    retention configurable up to 2 years, higher cost per GB but queryable
  - Storage Account: cheapest long-term archival, NOT queryable in real time
Best practice: both -- Log Analytics for active monitoring, Storage for archival.

Q2 -- KQL query: sign-ins from multiple countries in 24h
  SignInLogs
  | where ResultType == 0  // successful sign-ins only
  | extend Country = tostring(LocationDetails.countryOrRegion)
  | summarize Countries = dcount(Country), CountryList = make_set(Country)
      by UserPrincipalName, bin(TimeGenerated, 24h)
  | where Countries >= 3  // replace with chosen geo_count threshold
  | project TimeGenerated, UserPrincipalName, Countries, CountryList
  | order by Countries desc

Q3 -- Built-in Entra Workbooks
Path for all: Entra admin centre > Monitoring > Workbooks.
  a) Legacy authentication: "Sign-ins using legacy authentication"
     (shows users, protocols, apps still using Basic auth)
  b) CA impact before enforcement: "Conditional Access Insights and Reporting"
     (shows report-only policy results and impact analysis)
  c) Risky sign-ins over time: "Microsoft Entra ID Protection" workbook
     or the Risky sign-ins report under Identity Protection

Q4 -- Secure Score improvement actions
"Require MFA for administrative roles":
  Create CA policy: Assignments = directory roles (all admin roles) >
  Grant = Require MFA. This is the primary control Microsoft measures.
"Enable self-service password reset":
  Path: Entra > Security > Password reset > Self-service password reset = All.
  Reduces helpdesk load and enables risk policy password reset remediation.
"Do not expire passwords":
  Microsoft research: expiry causes weaker passwords (Password1! -> Password2!).
  Rely on breach detection (ID Protection) instead of forced rotation.
  Path: Entra > Users > Password expiration policy > Never expire.
  (Also configurable via Microsoft 365 admin centre or PowerShell.)

Q5 -- Investigating a potentially compromised account
1. Entra admin centre > Users > [user] > Sign-in logs
2. Filter: last 7-30 days, Status = All (include failures)
3. Look for: unfamiliar IPs, unusual locations, new device/browser,
   sign-ins at unusual hours, failed attempts followed by success
4. Click suspicious sign-in: review IP, location, device ID, app accessed,
   CA policies applied, risk level flagged by ID Protection
5. Entra admin centre > Users > [user] > Audit logs
   Look for: role assignments, group changes, app consent grants,
   MFA method additions (attacker registering their own MFA device)
6. If compromised: Revoke all sessions > reset password > review and remove
   any new MFA methods registered > check for new OAuth app consent grants
   (Entra > Enterprise apps > filter by consent date)
"""
    },
]

ALL_SC300_SCENARIOS = (
    DOMAIN1_SCENARIOS +
    DOMAIN2_SCENARIOS +
    DOMAIN3_SCENARIOS +
    DOMAIN4_SCENARIOS
)

def generate_sc300_pbq(domain_filter=None, difficulty_filter=None):
    pool = ALL_SC300_SCENARIOS
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
    domain_info = SC300_EXAM["domains"][template["domain"]]
    return {
        "exam":            f"{SC300_EXAM['name']} ({SC300_EXAM['code']})",
        "id":              template["id"],
        "domain":          f"{template['domain']}. {domain_info['name']} ({domain_info['weight']}%)",
        "sub_topic":       template["sub_topic"],
        "objective":       template["objective"],
        "difficulty":      template["difficulty"],
        "exam_objectives": ", ".join(template.get("exam_objectives", [])),
        "scenario":        scenario_text.strip(),
        "answers":         template.get("answers", "No answers available."),
    }

def get_weighted_sc300_pbq():
    weights = [22, 28, 22, 28]
    domain = random.choices(["1", "2", "3", "4"], weights=weights, k=1)[0]
    return generate_sc300_pbq(domain_filter=domain)

def display_sc300_pbq(pbq: dict, student_mode: bool = False):
    separator = "=" * 70
    print(f"\n{separator}")
    print(f"  {pbq.get('exam', 'SC-300')}")
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
    print("\nGIDEON - SC-300 Module Test")
    print("Generating 3 sample PBQs (weighted by domain)...\n")
    for i in range(3):
        pbq = get_weighted_sc300_pbq()
        display_sc300_pbq(pbq, student_mode=False)
        input("Press ENTER for next scenario...\n")

