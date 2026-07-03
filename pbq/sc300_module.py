"""
GIDEON SC-300 Module
====================
Microsoft Identity and Access Administrator (SC-300)
Exam domains and weights (2025-01):
  1. Implement and Manage User Identities         25-30%
  2. Implement Authentication and Access Mgmt     25-30%
  3. Plan and Implement Workload Identities       25-30%
  4. Plan and Automate Identity Governance        25-30%
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
        "4": {"name": "Plan and Automate Identity Governance",         "weight": "25-30"},
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

"""
GIDEON SC-300 Domain 2 — Additional Scenario Templates
Replace the existing DOMAIN2_SCENARIOS list in sc300_module.py with this.
Each scenario ID now has 3 templates — tripling variety.
"""

# ════════════════════════════════════════════════════════════════════════════
# SC2-001: Conditional Access Policy Design — 3 templates
# ════════════════════════════════════════════════════════════════════════════

SC2_001_TEMPLATES = [

    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC2-001",
        "template_variant": "A",
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
ANSWER GUIDE -- SC2-001-A: Conditional Access Policy Design

Q1 -- Report-only mode
Create policy in Report-only mode. Monitor: Entra admin centre > Monitoring >
Sign-in logs > filter by CA policy name > review "Report-only" column.
Check for: service accounts, legacy auth clients, shared mailboxes, break-glass
accounts being impacted. Switch to "On" only when zero legitimate users show as
"would fail."

Q2 -- Policy for compliant devices on corp network
Assignments: Users = All users (exclude admins), Cloud apps = Office 365.
Conditions: Named location = corp IP range (trusted), Device = compliant.
Grant: Require device marked as compliant OR Hybrid Entra joined (OR logic).
Named location: Entra > Security > CA > Named locations > IP ranges location.
Mark as trusted location.

Q3 -- Authentication Context
Standard CA targets an entire app. Authentication Context targets a SPECIFIC
ACTION within an app. The app developer calls the auth context ID in their code
when the sensitive action is triggered. A separate CA policy enforces stricter
controls only when that context fires.
Path: Entra > Security > CA > Authentication context > Add.

Q4 -- Legacy authentication discovery
Run the "Sign-ins using legacy authentication" workbook:
Entra admin centre > Monitoring > Workbooks > Legacy Authentication.
Shows users, apps, and protocols (SMTP AUTH, POP3, IMAP) still using basic auth.
Remediate these BEFORE blocking -- otherwise legitimate services break.

Q5 -- Service account exclusion risk and compensating control
Risk: excluded accounts bypass all CA policies.
Compensating control: create a dedicated CA policy for the service account
that ONLY allows sign-in from specific named IP locations (server IPs).
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

    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC2-001",
        "template_variant": "B",
        "domain": "2",
        "sub_topic": "Conditional Access Policy Design",
        "objective": "2.2 - Plan, implement, and manage Microsoft Entra Conditional Access",
        "scenario_template": """
{org_name} has {num_ca_policies} Conditional Access policies configured but is
experiencing the following problems:

  - {num_locked_out} users were locked out last week after a policy change
  - Guest users from {partner_org} cannot access the Teams tenant
  - A CA policy targeting {sensitive_app} is blocking a legitimate service account
  - Sign-in logs show {num_legacy_auth} legacy authentication attempts per day
  - The security team cannot tell which CA policy is causing a specific block
  - Continuous Access Evaluation is not configured

Questions:
1. {num_locked_out} users were locked out after a policy change. Walk through
   the emergency recovery process. What tool do you use to identify exactly
   which policy caused the lockout? How do you temporarily disable a policy
   without deleting it?
2. Guest users from {partner_org} cannot access Teams. What CA policy conditions
   commonly block B2B guests that don't apply to internal users?
   How do you scope a policy to exclude or specifically target guest users?
3. A service account is being blocked by the {sensitive_app} CA policy.
   Walk through identifying the service account in sign-in logs and configuring
   a safe exclusion. What is the maximum recommended number of exclusions
   before a policy becomes unmanageable?
4. Configure a CA policy to block the {num_legacy_auth} legacy authentication
   attempts. What client app conditions do you select? What must you verify
   before enabling to avoid breaking legitimate services?
5. Explain Continuous Access Evaluation (CAE). What events trigger real-time
   token revocation? How does CAE differ from standard token lifetime policies?
6. The security team cannot identify which policy caused a block. Walk through
   using the CA policy details in sign-in logs to diagnose the issue.
   What does "Report-only: Would have failed" mean vs "Failure"?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Pacific Engineering", "Alpine Council"],
            "num_ca_policies": ["23", "14", "38", "9"],
            "num_locked_out": ["12", "34", "7", "48"],
            "partner_org": ["Pacific Rim Consulting", "Southern Cross Partners", "Alpine Advisory", "Bay Group"],
            "sensitive_app": ["Finance ERP", "Patient Records System", "HR Payroll Portal", "Legal Case Management"],
            "num_legacy_auth": ["340", "89", "512", "127"],
        },
        "exam_objectives": ["2.2"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-001-B: Conditional Access Troubleshooting

Q1 -- Emergency lockout recovery
If ALL admins are locked out: use break-glass account (excluded from all CA).
If some admins can still sign in:
  Entra > Security > Conditional Access > [policy] > toggle State to "Off."
  Do NOT delete -- disabling preserves the policy for review.
Identify the causing policy: Entra > Users > [locked out user] > Sign-in logs >
  find the failed sign-in > Conditional Access tab > look for "Failure" status.
  The policy name is shown alongside the result.
Post-recovery: use Report-only mode for future policy changes before enabling.

Q2 -- Guest user CA policy issues
Common causes:
  - Policy requires compliant device: guests use unmanaged personal devices
    which cannot be Intune-enrolled in the host tenant.
  - Policy requires hybrid Entra joined: guests are never hybrid joined to host.
  - Policy requires specific named location: guest's corporate IP is not in
    the host tenant's named locations.
Scoping for guests: Conditions > Users > Include = Guest or external users >
  select "B2B collaboration guest users."
Best practice: create a separate CA policy for guests with appropriate controls
(MFA required, no device compliance requirement since guests can't enrol).

Q3 -- Service account exclusion
Identify: Sign-in logs > filter by service account UPN > confirm which policy
is blocking (CA tab on the failed sign-in event).
Safe exclusion: add the service account to the policy's Exclude > Users list.
Maximum exclusions: Microsoft recommends keeping exclusions under 5 per policy.
Beyond that, create a separate policy targeting excluded accounts with
compensating controls (IP restriction, alert on sign-in outside approved IPs).

Q4 -- Blocking legacy authentication
CA policy: Conditions > Client apps > select:
  Exchange ActiveSync clients, Other clients (covers SMTP AUTH, POP3, IMAP, MAPI).
Grant: Block access.
Pre-checks: run "Sign-ins using legacy authentication" workbook first.
Common legitimate legacy auth sources to remediate before blocking:
  - Printers/scanners using SMTP AUTH to send email
  - Older mobile apps configured with basic auth
  - PowerShell scripts using basic auth credentials

Q5 -- Continuous Access Evaluation (CAE)
CAE enables real-time token revocation rather than waiting for token expiry.
Events that trigger immediate revocation:
  - User account disabled or deleted
  - Password changed or reset
  - MFA method changed
  - Admin explicitly revokes all sessions
  - High risk event detected by ID Protection
Standard token lifetime: access tokens valid for 60-90 minutes by default.
With CAE: token can be revoked within seconds of a triggering event.
CAE requires: supported client (Office apps, modern auth clients) and
the resource (Exchange, SharePoint, Teams) must support CAE.

Q6 -- Diagnosing CA blocks in sign-in logs
Path: Entra > Monitoring > Sign-in logs > find sign-in > Conditional Access tab.
Each policy applied shows: Policy name, Result, Grant controls applied.
Results:
  "Success" -- policy applied and access granted.
  "Failure" -- policy applied and access blocked (this is your culprit).
  "Not applied" -- policy conditions did not match this sign-in.
  "Report-only: Would have succeeded/failed" -- policy in report-only mode,
  shows what WOULD have happened if the policy were enabled.
"Report-only: Would have failed" means the policy would block the user if
switched to On -- useful for pre-deployment testing without actual impact.
"""
    },

    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC2-001",
        "template_variant": "C",
        "domain": "2",
        "sub_topic": "Conditional Access Policy Design",
        "objective": "2.2 - Plan, implement, and manage Microsoft Entra Conditional Access",
        "scenario_template": """
{org_name} is implementing a Zero Trust architecture and needs to redesign
their Conditional Access strategy from scratch.

Current state:
  - Only 2 CA policies exist: "Require MFA for all" and "Block legacy auth"
  - No device compliance policies configured in Intune
  - {num_remote_users} remote workers access resources from unmanaged devices
  - Executives ({num_execs} users) refuse additional authentication prompts
  - {sensitive_app} contains highly regulated data requiring step-up auth
  - No insider risk integration configured

Questions:
1. Design a complete CA policy architecture for Zero Trust. How many policies
   would you create and what is the logical grouping? What is the recommended
   maximum number of CA policies before management becomes unworkable?
2. Configure device compliance in Intune as a CA condition. What is the
   difference between "Require device to be marked as compliant" and
   "Require Hybrid Azure AD joined device"? Which suits {num_remote_users}
   remote workers on personal devices?
3. The {num_execs} executives refuse MFA prompts. What CA features reduce
   MFA friction for low-risk sign-ins without removing the MFA requirement?
   Name two specific CA conditions that reduce prompt frequency.
4. {sensitive_app} requires step-up authentication only when users access
   sensitive reports (not the whole app). Configure this using Authentication
   Context and explain the developer integration required.
5. Configure insider risk-based Conditional Access. What Microsoft service
   provides the insider risk signal? What CA condition consumes it and what
   action do you trigger for medium vs high insider risk?
6. Design the named location strategy for {org_name}. What is the difference
   between IP-based and country-based named locations? When would you use
   each and what are the limitations of country-based locations?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Insurance", "Alpine Manufacturing"],
            "num_remote_users": ["340", "89", "512", "127"],
            "num_execs": ["12", "8", "20", "5"],
            "sensitive_app": ["Finance ERP", "Patient Records System", "HR Payroll Portal", "Legal Case Management"],
        },
        "exam_objectives": ["2.2"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-001-C: Zero Trust CA Architecture

Q1 -- CA policy architecture for Zero Trust
Recommended grouping (8-12 policies):
  Group 1 - Baseline (all users): Block legacy auth, Require MFA for all
  Group 2 - Admins: Require phishing-resistant MFA, require compliant/PAW device
  Group 3 - Device state: Grant access for compliant devices, restrict unmanaged
  Group 4 - App-specific: Sensitive apps require compliant device + MFA
  Group 5 - Guests/external: Separate MFA policy, no device compliance required
  Group 6 - Risk-based: Block high risk sign-in, require MFA for medium risk
Microsoft recommends under 20 policies for manageability.
Use naming convention: [ORG]-[GROUP]-[PURPOSE]-[STATE] e.g. CONTOSO-ALL-BLOCK-LEGACY-ON

Q2 -- Device compliance conditions
"Require device marked as compliant": device must be enrolled in Intune and
meet the compliance policy (PIN, encryption, OS version etc).
Suits: corporate-owned devices enrolled in Intune.
"Require Hybrid Entra joined": device must be domain-joined AND synced to Entra.
Suits: traditional on-premises domain-joined corporate PCs.
For remote workers on personal devices: neither option works directly.
Options: (1) enrol personal devices in Intune under BYOD policy, or
(2) use app protection policies (MAM without enrollment) as an alternative
condition -- requires compliant app (Outlook, Teams) rather than compliant device.

Q3 -- Reducing MFA friction for executives
Two CA conditions that reduce prompt frequency:
1. Sign-in frequency: set to longer intervals (e.g. 7 days) for low-risk users
   on compliant devices. CA > Session controls > Sign-in frequency.
2. Persistent browser session: allows users to stay signed in across browser
   sessions on compliant devices. CA > Session controls > Persistent browser session.
Also: Token protection (preview) binds tokens to the specific device,
reducing the need for re-authentication when the device is trusted.

Q4 -- Authentication Context for step-up auth
Path: Entra > Security > CA > Authentication context > New authentication context.
Create context: e.g. "c1" labelled "Sensitive Reports Access."
CA policy: Conditions > Authentication context = c1 > Grant = Require MFA + compliant device.
Developer integration required: the application code must call the auth context
when the user navigates to the sensitive reports section:
  - Web app: include acr_values=c1 in the OAuth 2.0 authorization request
  - The app checks the acr claim in the returned token to confirm step-up completed
Without developer integration, the context never fires -- it cannot be applied
to an app that hasn't implemented the trigger.

Q5 -- Insider risk-based CA
Service: Microsoft Purview Insider Risk Management generates the risk signal.
CA condition: Conditions > Insider risk (preview) > select risk levels.
Actions:
  Medium insider risk: require MFA step-up or restrict to compliant device only.
  High insider risk: block access entirely or limit to read-only (app enforced).
Licence required: Microsoft 365 E5 or Microsoft 365 E5 Compliance.
Note: insider risk signal can take up to 24 hours to update in CA.

Q6 -- Named location strategy
IP-based named locations: define specific IP ranges (corporate office, VPN exit nodes).
  Use for: trusted locations that grant reduced MFA friction.
  Limitation: requires maintaining IP list as network changes.
Country-based named locations: define allowed or blocked countries.
  Use for: blocking sign-ins from countries where org has no presence.
  Limitation: VPNs and Tor exit nodes can spoof country -- not reliable as
  sole control. Use as additional signal, not primary control.
Best practice: combine both -- trusted IP ranges for reduced friction,
country block for obvious geographic anomalies.
"""
    },
]

# ════════════════════════════════════════════════════════════════════════════
# SC2-002: Authentication Methods and MFA — 3 templates
# ════════════════════════════════════════════════════════════════════════════

SC2_002_TEMPLATES = [

    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC2-002",
        "template_variant": "A",
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
ANSWER GUIDE -- SC2-002-A: Authentication Methods and MFA

Q1 -- Per-user MFA vs Authentication Methods policy
Per-user MFA (legacy): configured per-user in M365 admin centre, separate
from Conditional Access, limited method control.
Authentication Methods policy (modern): Entra > Security > Authentication methods.
Controls which methods are available tenant-wide, integrates with CA and ID Protection.
To avoid conflicts: disable legacy per-user MFA settings AND disable Security
defaults before enabling CA-based MFA.

Q2 -- Migration from SMS OTP to Authenticator
Phase 1: Enable Authenticator in Authentication Methods policy.
  Enable registration campaign to nudge users at next sign-in.
Phase 2: Set Authenticator as default method for enrolled users.
Phase 3: Disable SMS OTP in Authentication Methods policy.
For resistant executives: escalate to CISO, frame as SIM swap risk.
Offer FIDO2 security key as alternative. Document risk acceptance if refused.

Q3 -- MFA without a smartphone
Options: FIDO2 security key, Temporary Access Pass (TAP),
Certificate-based authentication, Windows Hello for Business.
Recommendation for field workers: FIDO2 security keys.

Q4 -- SSPR cost and configuration
Annual cost = monthly resets x cost per reset x 12.
Configure: Entra > Security > Password reset > Self-service password reset = All.
Require 2 authentication methods.
Recommended for regulated sectors: Microsoft Authenticator + email to personal address.
Avoid SMS as a method due to SIM swap risk.

Q5 -- Windows Hello for Business
Prerequisites: Windows 10/11, Entra joined or Hybrid Entra joined,
Entra ID P1 minimum, MFA registration completed.
WHfB replaces: passwords for Windows sign-in and browser/app authentication.
Phishing resistance: uses asymmetric key cryptography. Private key never leaves
the device (protected by TPM). No password or OTP to intercept.
"""
    },

    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC2-002",
        "template_variant": "B",
        "domain": "2",
        "sub_topic": "Authentication Methods and MFA",
        "objective": "2.1 - Plan, implement, and manage Microsoft Entra user authentication",
        "scenario_template": """
{org_name} has completed MFA rollout but is now experiencing authentication
problems and wants to strengthen their passwordless strategy.

Current issues:
  - {num_mfa_fatigue} users have reported MFA fatigue attacks in the past month
  - {num_tap_requests} helpdesk tickets per week for MFA lockouts and resets
  - Passwordless authentication is not deployed
  - {num_shared_devices} shared workstations in {shared_location} have no
    suitable authentication method
  - Certificate-based authentication (CBA) is required for {privileged_group}
  - Temporary Access Pass (TAP) is not configured

Questions:
1. {num_mfa_fatigue} users experienced MFA fatigue attacks. What specific
   Authenticator feature prevents MFA fatigue? How do you enable it and
   what does the user experience look like compared to standard push notifications?
2. Design a passwordless deployment plan for {org_name}. What are the three
   Microsoft passwordless options in order of phishing resistance?
   Which is most suitable for {shared_location} shared workstations?
3. Configure Temporary Access Pass (TAP) for MFA lockout recovery.
   What are the TAP settings you must configure? Can a TAP be used to
   register a FIDO2 key and why is this important?
4. {privileged_group} requires certificate-based authentication. What
   infrastructure is required for CBA? What is the difference between
   single-factor and multi-factor CBA certificates?
5. The {num_tap_requests} weekly MFA lockout tickets indicate a process problem.
   Design a self-service MFA recovery flow using TAP that reduces helpdesk
   involvement. What security controls prevent TAP abuse?
6. Configure the Authentication Methods policy to enable passwordless phone
   sign-in for all users. What is the difference between enabling a method
   in Authentication Methods policy vs enabling it in the legacy MFA portal?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Insurance", "Alpine Engineering"],
            "num_mfa_fatigue": ["8", "23", "4", "15"],
            "num_tap_requests": ["45", "12", "78", "6"],
            "num_shared_devices": ["34", "89", "12", "56"],
            "shared_location": ["hospital wards", "factory floor", "retail branches", "call centre"],
            "privileged_group": ["Global Administrators", "Security Operations team", "Finance Controllers", "Clinical Systems Admins"],
        },
        "exam_objectives": ["2.1"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-002-B: Passwordless and Advanced Authentication

Q1 -- MFA fatigue prevention
Feature: Number matching in Microsoft Authenticator.
How it works: instead of a simple Approve/Deny push, the user must type a
2-digit number displayed on the sign-in screen into the Authenticator app.
An attacker sending fraudulent push notifications cannot trick the user into
approving because they don't know the number.
Enable: Entra > Security > Authentication methods > Microsoft Authenticator >
Configure > Number matching = Enabled.
Also enable: Additional context (shows app name and location in the push).
User experience: push arrives, user sees "Enter the number shown: 42" instead
of just Approve/Deny.

Q2 -- Passwordless options in order of phishing resistance
1. FIDO2 security keys (highest) -- hardware bound, origin validated,
   immune to phishing and MFA fatigue. Best for shared workstations.
2. Windows Hello for Business -- TPM-bound, biometric/PIN, phishing resistant.
   Best for dedicated corporate Windows devices.
3. Microsoft Authenticator passwordless phone sign-in -- app-based,
   phishing resistant but phone can be lost/stolen.
For shared workstations in {shared_location}: FIDO2 security keys --
users carry their key, tap to log in, tap to log out. No phone needed.

Q3 -- Temporary Access Pass (TAP) configuration
Path: Entra > Security > Authentication methods > Temporary Access Pass > Enable.
Settings to configure:
  - Minimum lifetime: 10 minutes (for immediate use)
  - Maximum lifetime: up to 8 hours (for onboarding scenarios)
  - One-time use: Yes (for security -- single use TAP cannot be reused)
  - Length: 8 characters minimum
TAP and FIDO2 registration: Yes -- a TAP can be used to register a FIDO2
security key. This is the recommended onboarding flow:
  IT generates TAP > user signs in with TAP > registers FIDO2 key >
  TAP expires and user authenticates with FIDO2 going forward.
This avoids the bootstrapping problem of "need MFA to register MFA."

Q4 -- Certificate-based authentication (CBA)
Infrastructure required:
  - On-premises PKI (Certificate Authority) or cloud PKI
  - Root/intermediate CA certificates uploaded to Entra ID
  - User certificates issued with correct Subject Alternative Name (UPN)
Single-factor CBA: certificate alone satisfies one authentication factor.
  User still needs MFA for high-privilege operations.
Multi-factor CBA: certificate is configured to satisfy MFA requirement directly.
  No additional MFA prompt -- the certificate IS the MFA.
  Requires: certificate policy OID mapped to MFA in Entra CBA settings.
Use case for privileged group: multi-factor CBA so admins authenticate with
smartcard/hardware token and are not prompted for additional MFA.

Q5 -- Self-service MFA recovery with TAP
Flow design:
  1. User reports MFA lockout via helpdesk portal or manager request
  2. Helpdesk generates time-limited one-time TAP in Entra admin centre
  3. TAP delivered to user via verified secondary channel (manager email/phone)
  4. User signs in with TAP, immediately registers new MFA method
  5. TAP expires, user continues with new MFA method
Security controls preventing TAP abuse:
  - One-time use: cannot be reused after first sign-in
  - Short lifetime: configure 1-4 hours maximum
  - Audit log: every TAP issuance logged with issuer and recipient
  - Require manager approval before helpdesk can generate TAP

Q6 -- Authentication Methods policy vs legacy MFA portal
Authentication Methods policy (Entra > Security > Authentication methods):
  Modern, per-method enablement, supports targeting specific user groups,
  integrates with registration campaigns and Authenticator features.
Legacy MFA portal (per-user MFA in M365 admin centre):
  Old interface, tenant-wide only, limited method control, being deprecated.
Key difference: enabling passwordless phone sign-in in the Authentication
Methods policy is the ONLY supported way in modern Entra ID.
The legacy portal does not support passwordless configuration.
Always use Authentication Methods policy -- disable the legacy portal settings
to avoid conflicts (Security defaults must also be off).
"""
    },

    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC2-002",
        "template_variant": "C",
        "domain": "2",
        "sub_topic": "Authentication Methods and MFA",
        "objective": "2.1 - Plan, implement, and manage Microsoft Entra user authentication",
        "scenario_template": """
{org_name} is preparing for an external security audit. The auditor has
flagged the following authentication weaknesses:

  - SSPR is enabled but {num_sspr_abuse} accounts show suspicious SSPR activity
  - Authentication methods registration is not being monitored
  - {num_unregistered} users have no MFA method registered
  - The organisation relies on a single MFA method per user (no backup method)
  - Voice call authentication is still enabled despite phishing risk
  - No registration campaign has been configured

Questions:
1. {num_sspr_abuse} accounts show suspicious SSPR activity. What specific
   report in Entra ID shows SSPR usage and abuse patterns? What constitutes
   suspicious SSPR activity and what immediate action do you take?
2. Configure an authentication method registration campaign for the
   {num_unregistered} unregistered users. What happens to users who
   repeatedly dismiss the registration prompt? How long can they snooze it?
3. Design a backup authentication method policy. Why is a single registered
   method a security and usability risk? What is Microsoft's recommendation
   for minimum number of registered methods per user?
4. Voice call authentication is enabled. Why is this a security risk?
   Walk through disabling it in the Authentication Methods policy without
   disrupting users who currently use it as their only method.
5. Configure the Authentication Methods activity report to monitor
   registration health. What metrics would you track weekly and what
   threshold would trigger an escalation to the security team?
6. {org_name} wants to enforce that all users register at least two
   authentication methods within {registration_deadline} days.
   Design the enforcement strategy using CA policies and registration
   campaigns. What happens to users who do not comply by the deadline?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Council", "Pacific Finance", "Alpine Manufacturing"],
            "num_sspr_abuse": ["12", "4", "23", "7"],
            "num_unregistered": ["89", "234", "34", "156"],
            "registration_deadline": ["14", "30", "7", "21"],
        },
        "exam_objectives": ["2.1"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC2-002-C: Authentication Audit and Compliance

Q1 -- SSPR abuse detection
Report: Entra admin centre > Protection > Password reset > Activity tab.
Shows: SSPR attempts, successes, failures by user and method.
Also: Entra > Monitoring > Audit logs > filter Activity = "Reset password (self-service)."
Suspicious SSPR activity indicators:
  - Multiple SSPR attempts in short timeframe (attacker trying to reset)
  - SSPR completed from unusual location/IP
  - SSPR completed then immediate sign-in from different location
Immediate action: review the account's sign-in logs, check for new MFA methods
registered after SSPR, revoke sessions, and consider temporarily disabling
the account pending investigation.

Q2 -- Registration campaign configuration
Path: Entra > Security > Authentication methods > Registration campaign.
State: Enabled. Days allowed to snooze: set to 1-3 days.
What happens when users dismiss:
  - Users can snooze for the configured number of days
  - After the maximum snooze count is reached, they CANNOT complete sign-in
    until they register -- they are forced to the registration experience
  - Maximum snooze: configurable, typically 14 days total before enforcement
Users cannot permanently avoid registration once the campaign is enforced.

Q3 -- Backup authentication method policy
Single method risk:
  - Security: if method is compromised (SIM swap for SMS), account is lost
  - Usability: if phone is lost/broken, user is locked out
Microsoft recommendation: minimum 2 registered methods per user.
Enforcement: Authentication Methods policy does not directly enforce this,
but the registration campaign can be configured to prompt for a second method.
Monitor compliance: Entra > Protection > Authentication methods activity >
"Users registered for MFA" report -- shows how many methods each user has.

Q4 -- Disabling voice call authentication safely
Risk: voice calls are susceptible to SIM swapping and social engineering.
Attackers can port a phone number and receive voice MFA calls.
Safe removal process:
  Step 1: Run Authentication Methods activity report -- identify users who
    have voice call as their ONLY registered method.
  Step 2: Run registration campaign targeting those users to add Authenticator.
  Step 3: Wait for compliance (14-30 days with helpdesk support available).
  Step 4: Disable voice call in Authentication Methods policy.
Path: Entra > Security > Authentication methods > Voice call > Disable.
Do NOT disable before step 3 -- users with voice as only method will be locked out.

Q5 -- Authentication Methods activity monitoring
Path: Entra > Protection > Authentication methods activity.
Weekly metrics to track:
  - % users registered for MFA (target: 100%)
  - % users registered for passwordless (track improvement over time)
  - % users with 2+ methods (target: 100%)
  - SSPR registration % (target: 100% of SSPR-enabled users)
Escalation threshold: any metric dropping more than 5% week-over-week,
or MFA registration falling below 95%.

Q6 -- Enforcement strategy for registration deadline
Phase 1 (immediate): Enable registration campaign, snooze = 3 days.
  Notify users via email that registration is required within deadline.
Phase 2 (day 7): Create CA policy in report-only mode:
  Condition: Registration status = not registered for MFA.
  Grant: Require MFA (this forces the registration experience).
Phase 3 (deadline day): Switch CA policy to On.
  Users without MFA registration cannot complete sign-in.
  They are redirected to the MFA registration page before accessing any app.
  Helpdesk generates TAP for users with genuine blockers (no smartphone etc).
Outcome: compliance is enforced technically, not just by policy communication.
"""
    },
]

# ════════════════════════════════════════════════════════════════════════════
# SC2-003: Microsoft Entra ID Protection — 3 templates
# ════════════════════════════════════════════════════════════════════════════

SC2_003_TEMPLATES = [

    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC2-003",
        "template_variant": "A",
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
ANSWER GUIDE -- SC2-003-A: Microsoft Entra ID Protection

Q1 -- User Risk vs Sign-in Risk
User Risk: probability that an identity is compromised. Accumulates over time.
Triggered by: leaked credentials, unusual activity patterns, admin confirmation.
Sign-in Risk: probability a specific authentication attempt is not from the
legitimate user. Per-sign-in.
Triggered by: anonymous IP, atypical travel, unfamiliar sign-in properties.
Risk levels: Low -> log. Medium -> require MFA. High -> block or force reset.

Q2 -- Risk-based CA policy
Use Conditional Access risk-based policies (modern approach).
Legacy ID Protection policies are being deprecated.
Configure: Entra > Security > CA > New policy > Conditions: User risk = High >
Grant: Require password change (requires SSPR to be enabled first).

Q3 -- Impossible travel investigation
1. Entra > Security > Identity Protection > Risky sign-ins
2. Find the CFO sign-in > review: IP, location, device, browser
3. CFO confirmed Auckland -- select "Confirm compromised" (NOT "Dismiss")
"Confirm compromised" -> sets user risk to High, triggers risk policy,
forces password reset, invalidates ALL active sessions.
"Dismiss user risk" -> clears risk flag (use ONLY for confirmed false positives).

Q4 -- MFA Registration Campaign
Path: Entra > Security > Authentication methods > Registration campaign.
State = Enabled, Days allowed to snooze = 1-14 days.
Users who dismiss are prompted again after the snooze period.
After configured snoozes they CANNOT complete sign-in until they register.

Q5 -- Risky workload identities
Licence: Microsoft Entra ID P2 (Workload Identities Premium add-on may be required).
Detections for workload identities: suspicious sign-ins, anomalous SP activity,
leaked credentials (client secrets in public repos).
NOT available: impossible travel, unfamiliar sign-in properties.
"""
    },

    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC2-003",
        "template_variant": "B",
        "domain": "2",
        "sub_topic": "Microsoft Entra ID Protection",
        "objective": "2.3 - Manage risk by using Microsoft Entra ID Protection",
        "scenario_template": """
{org_name} has had ID Protection enabled for {months_active} months but the
security team believes it is not configured optimally.

Current state:
  - {num_false_positives} risk detections per week are being dismissed as false positives
  - No risk-based CA policies are configured -- all risks are managed manually
  - {num_stale_risky} users have been at HIGH risk for over 30 days with no remediation
  - ID Protection reports are not being reviewed regularly
  - A password spray attack targeting {num_targeted} accounts was detected
    but no automated response fired

Questions:
1. {num_false_positives} weekly false positives suggest misconfiguration.
   What are the most common causes of false positive risk detections in ID Protection?
   How do you tune ID Protection to reduce false positives without missing real threats?
2. Configure risk-based CA policies to replace manual remediation.
   Design the complete policy set for: LOW, MEDIUM, and HIGH user risk,
   and LOW, MEDIUM, and HIGH sign-in risk. What action does each trigger?
3. {num_stale_risky} users have been HIGH risk for 30+ days. Why is this
   dangerous? Walk through bulk remediation of stale risky users.
   What is the difference between "Dismiss user risk" and "Confirm safe"?
4. The password spray attack triggered a detection but no automated response
   fired. What CA policy should have fired and what was likely misconfigured?
   What is the specific ID Protection detection name for password spray?
5. Design a weekly ID Protection review process. What four reports would you
   review, what metrics would you track, and what actions would each report
   drive? Who in the organisation should own this review?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Alpine Engineering", "Pacific Council"],
            "months_active": ["3", "6", "12", "1"],
            "num_false_positives": ["45", "12", "78", "6"],
            "num_stale_risky": ["8", "23", "4", "15"],
            "num_targeted": ["34", "89", "12", "56"],
        },
        "exam_objectives": ["2.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-003-B: ID Protection Optimisation

Q1 -- False positive causes and tuning
Common causes:
  - VPN exit nodes flagged as anonymous IP (users legitimately using VPN)
  - Business travel flagged as atypical travel or impossible travel
  - Shared service accounts triggering unfamiliar sign-in properties
  - Bulk operations (migrations, scripted tasks) appearing as anomalous
Tuning approaches:
  - Named locations: add VPN exit IPs and office IPs as trusted locations --
    sign-ins from trusted IPs are excluded from anonymous IP detection
  - Confirm safe: for legitimate risky sign-ins, use "Confirm safe" rather
    than dismiss -- this trains the ML model for your environment
  - Investigate before dismissing: review each false positive type and address
    the root cause (e.g. move service accounts to Managed Identities)

Q2 -- Risk-based CA policy set
Sign-in risk LOW: Allow with standard controls (no additional action)
Sign-in risk MEDIUM: Require MFA step-up
Sign-in risk HIGH: Block access OR require MFA + password change
User risk LOW: Allow with standard controls (monitor)
User risk MEDIUM: Require MFA on next sign-in
User risk HIGH: Require password change (block until SSPR completed)
Path for all: Entra > Security > Conditional Access > New policy >
Conditions > User risk or Sign-in risk > select level > Grant controls.
Note: "Require password change" grant requires SSPR to be enabled and
the user must have registered SSPR methods.

Q3 -- Stale HIGH risk users
Risk: HIGH risk users with no remediation may have been compromised for 30+
days. Attacker maintains persistent access while risk sits unactioned.
Bulk remediation: Entra > Security > Identity Protection > Risky users >
filter by Risk level = High, Risk state = At risk > select all > choose action.
"Confirm safe" vs "Dismiss user risk":
  Confirm safe: marks the sign-in as legitimate AND provides signal to the
    ML model that this type of activity is normal for this user.
  Dismiss user risk: clears the risk flag without providing ML feedback.
  Use "Confirm safe" for verified false positives; "Dismiss" for edge cases
  where you cannot fully verify but need to clear the flag.

Q4 -- Password spray missed response
Password spray detection name: "Password spray" (sign-in risk detection).
Why no response fired: most likely the sign-in risk CA policy was either
not configured, set to report-only, or the risk threshold was set too high.
Password spray sets sign-in risk to HIGH -- a HIGH sign-in risk CA policy
set to "Block access" would have prevented successful authentication.
Also check: were the targeted accounts excluded from the risk policy?
Common mistake: excluding service accounts from ALL CA policies including
risk-based ones -- attackers target these specifically.

Q5 -- Weekly ID Protection review process
Four reports to review:
1. Risky users report: new HIGH risk users this week, stale risks >7 days.
   Action: remediate HIGH, investigate MEDIUM.
2. Risky sign-ins report: volume trend, top detection types, unfamiliar locations.
   Action: tune named locations if VPN false positives, investigate clusters.
3. Risk detections report: new detection types appearing, volume per detection.
   Action: if new detection type appears, investigate root cause immediately.
4. ID Protection overview dashboard: risk score trend, coverage metrics.
   Action: track week-over-week improvement in risk posture.
Owner: Security Operations team with escalation path to CISO for HIGH risk
accounts belonging to executives or privileged users.
"""
    },

    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC2-003",
        "template_variant": "C",
        "domain": "2",
        "sub_topic": "Microsoft Entra ID Protection",
        "objective": "2.3 - Manage risk by using Microsoft Entra ID Protection",
        "scenario_template": """
A security incident at {org_name} has revealed that {compromised_account}
was compromised for an estimated {compromise_duration} before detection.

Post-incident findings:
  - ID Protection had flagged the account as MEDIUM risk {days_before} days
    before the breach was confirmed but no action was taken
  - The attacker used the compromised account to access {accessed_resource}
  - {num_lateral} other accounts showed suspicious activity during the same period
  - Leaked credentials detection fired but was dismissed as a false positive
  - No sign-in risk policy was configured for the affected user group

Questions:
1. Conduct a post-incident ID Protection review. What sequence of reports
   and logs would you pull to reconstruct the attacker's timeline?
   What is the first action you take for the {num_lateral} other accounts?
2. The MEDIUM risk flag was ignored {days_before} days before breach. Design
   a risk escalation and response SLA policy. What response time and action
   is appropriate for each risk level (Low, Medium, High)?
3. Leaked credentials detection was dismissed as a false positive. What is
   this detection and how does Microsoft discover leaked credentials?
   What makes a real leaked credential detection look different from a
   false positive and how should you verify before dismissing?
4. Configure sign-in risk policies that would have detected and stopped
   this attack. What specific combination of detection type and CA policy
   would have blocked the attacker while allowing the legitimate user to
   recover access?
5. {org_name} wants to implement ID Protection for workload identities to
   prevent similar attacks via service principals. What licence is required?
   Configure a workload identity risk policy and explain what happens when
   a service principal is flagged as HIGH risk.
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Insurance", "Alpine Manufacturing"],
            "compromised_account": ["a Finance Manager account", "an IT Administrator account", "a Clinical Systems account", "an HR Manager account"],
            "compromise_duration": ["14 days", "21 days", "7 days", "30 days"],
            "days_before": ["14", "7", "21", "10"],
            "accessed_resource": ["the payroll system", "patient records", "the Azure subscription", "the HR database"],
            "num_lateral": ["3", "8", "2", "12"],
        },
        "exam_objectives": ["2.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-003-C: Post-Incident ID Protection Review

Q1 -- Post-incident timeline reconstruction
Sequence of reports to pull:
1. Entra > Security > Identity Protection > Risky users > [compromised account]
   > Risk history -- shows when risk was first detected and all state changes
2. Entra > Security > Identity Protection > Risk detections -- filter by user,
   shows every detection with timestamp, detection type, and risk level
3. Entra > Users > [account] > Sign-in logs -- full sign-in history including
   successful and failed attempts, IPs, locations, apps accessed
4. Entra > Users > [account] > Audit logs -- role assignments, group changes,
   app consent grants made during the compromise period
First action for the other suspicious accounts:
  Immediately revoke sessions for all (Entra > Users > [user] > Revoke sessions)
  and set user risk to confirmed compromised. Do NOT wait for investigation --
  contain first, investigate second.

Q2 -- Risk response SLA policy
LOW risk: Review within 5 business days. Action: monitor, no immediate response.
MEDIUM risk: Review within 24 hours. Action: require MFA step-up at next sign-in,
  notify account owner's manager, add to watch list for 7 days.
HIGH risk: Respond within 1 hour (automated preferred). Action: block sign-in,
  force password reset via SSPR, revoke all active sessions, notify security team.
Automation: CA risk-based policies handle HIGH and MEDIUM automatically.
Manual SLA applies to LOW and to HIGH events that require human investigation
beyond the automated CA response.

Q3 -- Leaked credentials detection
What it is: Microsoft monitors dark web forums, paste sites, hacker marketplaces,
and partners with threat intelligence services to find credential dumps.
When a username/password pair matching an Entra ID account is found,
the leaked credentials detection fires.
Real vs false positive:
  Real: the exact UPN and a password that matches (or recently matched) the
    account's password hash. Microsoft validates before flagging.
  False positive: another account with a similar UPN was found in a breach
    (e.g. same username at a different domain from a personal account).
Verification before dismissing:
  1. Check the user's password history -- did they reuse a password?
  2. Check breach databases (HaveIBeenPwned) for the user's email address
  3. Ask the user directly if they reuse passwords across personal/work accounts
  Never dismiss leaked credentials without verification -- it is one of the
  highest confidence detections in ID Protection.

Q4 -- Preventive CA policy configuration
The attacker used compromised credentials (leaked credential detection fires).
Detection type: Leaked credentials -> sets USER RISK to HIGH.
CA policy that would have stopped it:
  User risk = High > Grant = Require password change
This blocks all sign-ins for the user until they complete SSPR.
The attacker cannot complete SSPR (they don't control the registered methods).
The legitimate user can: they receive an SSPR link, reset password,
risk is cleared, access restored.
Additionally: Sign-in risk = Medium/High > Grant = Require MFA
Would have caught the attacker at the sign-in level before user risk escalated.

Q5 -- Workload identity risk policy
Licence: Microsoft Entra Workload Identities Premium (add-on to P2).
Configure: Entra > Security > Identity Protection > Workload identity risk policies.
New policy > Select service principals > Risk level = High > Action = Block.
When a service principal is flagged HIGH risk:
  The service principal's sign-ins are blocked by the policy.
  All token requests from that SP are denied.
  Security team is notified via the risk detection alert.
  Investigation: check if client secret was leaked (GitHub scanning detection),
  rotate the secret/certificate, investigate what the SP accessed during the
  risk window, then dismiss the risk after remediation.
"""
    },
]

# ════════════════════════════════════════════════════════════════════════════
# SC2-004: Global Secure Access — 3 templates
# ════════════════════════════════════════════════════════════════════════════

SC2_004_TEMPLATES = [

    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC2-004",
        "template_variant": "A",
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
ANSWER GUIDE -- SC2-004-A: Global Secure Access

Q1 -- Private Access vs Internet Access
Private Access: ZTNA -- replaces VPN. Provides access to specific private
resources only, not the whole network. Zero lateral movement.
Internet Access: Secure Web Gateway for internet-bound traffic plus M365 optimisation.
To replace the legacy VPN -> deploy Private Access.

Q2 -- GSA client deployment
Prerequisites: Entra ID P1, device Entra joined or Hybrid Entra joined,
GSA enabled in Entra admin centre, Private Network Connector on-premises.
Deployment at scale for Windows: Microsoft Intune (Endpoint Manager).
Deploy GSA client MSI as Win32 app targeting the remote workers group.

Q3 -- Configuring Private Access
Step 1: Deploy Private Network Connector on-premises Windows Server.
  Download from: Global Secure Access > Connect > Connectors.
  Only outbound HTTPS required.
Step 2: Create Application Segment in Enterprise applications > New app.
  Add segment: FQDN or IP + port.
Step 3: Assign users/groups to the application.
Step 4: Create CA policy targeting the GSA app to enforce MFA + compliant device.

Q4 -- Microsoft 365 traffic profile
Global Secure Access > Traffic forwarding > Microsoft 365 access profile > Enable.
Uses Microsoft's optimised network paths, bypassing VPN hairpin.
Profile automatically includes correct M365 endpoints.

Q5 -- Verifying GSA usage
Global Secure Access > Monitor > Traffic logs -- filter by app name, user, connector.
Dashboard: Global Secure Access > Dashboard -- connected users, top apps, connector health.
Cross-check: VPN gateway logs should show drop in traffic volume after GSA deployment.
"""
    },

    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC2-004",
        "template_variant": "B",
        "domain": "2",
        "sub_topic": "Global Secure Access",
        "objective": "2.4 - Implement Global Secure Access",
        "scenario_template": """
{org_name} has deployed Global Secure Access but is experiencing issues:

  - {num_users_failing} users cannot connect to private apps through GSA
  - The Private Network Connector on {connector_server} shows as unhealthy
  - Microsoft 365 traffic is still going through the VPN despite GSA being enabled
  - {branch_office} branch office users need GSA without installing the client
  - Security team cannot see what private resources users are accessing
  - A user reported accessing a restricted site that should be blocked

Questions:
1. The Private Network Connector on {connector_server} is unhealthy. Walk through
   diagnosing and resolving connector health issues. What outbound ports and
   endpoints must be reachable from the connector server? What Windows service
   must be running?
2. {num_users_failing} users cannot connect through GSA. List the five most
   common causes of GSA client connection failure and how to diagnose each.
   What GSA client diagnostic tool is available?
3. M365 traffic is still going through the VPN despite the M365 traffic profile
   being enabled. What are the two most likely causes? How does GSA handle
   traffic forwarding in priority order when both VPN and GSA client are active?
4. {branch_office} branch office needs GSA without per-device client installation.
   What GSA feature supports this? What are the requirements and limitations
   compared to the full GSA client?
5. Configure internet access content filtering to block {blocked_category} sites.
   Walk through: creating a web content filtering policy, assigning it to users,
   and verifying blocked access in the logs.
6. A user accessed a restricted site that should be blocked. Investigate using
   GSA logs. What specific log type shows internet access traffic?
   How do you identify if the user bypassed GSA using a different network path?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Pacific Engineering", "Alpine Council"],
            "num_users_failing": ["34", "89", "12", "156"],
            "connector_server": ["gsa-connector01.contoso.local", "conn-srv01.fabrikam.internal", "gsaconn.alpine.lan"],
            "branch_office": ["Wellington", "Christchurch", "Hamilton", "Dunedin"],
            "blocked_category": ["social media", "gambling", "personal storage", "streaming media"],
        },
        "exam_objectives": ["2.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-004-B: GSA Troubleshooting

Q1 -- Connector health diagnosis
Connector health check path: Global Secure Access > Connect > Connectors > [connector].
Required outbound connectivity from connector server:
  - *.msappproxy.net port 443 (HTTPS)
  - *.servicebus.windows.net port 443
  - login.microsoftonline.com port 443
  No inbound ports required -- all connections are outbound.
Windows service: "Microsoft Entra private network connector" must be Running.
Check: Services.msc on the connector server.
Common causes: firewall blocking outbound, proxy requiring authentication,
TLS inspection breaking the connector's certificate validation.
Fix TLS inspection: add connector service to proxy bypass list.

Q2 -- GSA client connection failure causes
1. GSA client not running: check Task Manager for "Global Secure Access Client"
2. Device not Entra joined: GSA requires Entra join or Hybrid Entra join
3. No connector healthy in the connector group: check connector health dashboard
4. Application segment not configured: FQDN/IP not added to the private app
5. CA policy blocking the GSA app: check sign-in logs for the GSA enterprise app
Diagnostic tool: GSA client tray icon > Diagnostics > runs connectivity tests
and shows which checks pass/fail with specific error codes.

Q3 -- M365 traffic still going through VPN
Two most likely causes:
1. VPN split tunnelling not configured: VPN is capturing all traffic including
   M365 before GSA can intercept it. Configure VPN split tunnelling to exclude
   M365 IP ranges, allowing GSA to handle them.
2. Traffic forwarding profile not assigned to users: the M365 profile must be
   assigned to the user group, not just enabled globally.
Traffic priority order: when both VPN and GSA client are active, the VPN
typically wins if it captures traffic first (lower metric route).
Resolution: configure VPN to exclude M365 endpoints via split tunnelling,
or migrate users off VPN to GSA Private Access entirely.

Q4 -- Branch office without per-device client
Feature: Remote Network Connectivity (branch connectivity via IPsec/BGP tunnel).
Requirements: a router/firewall at the branch that supports IPsec IKEv2,
configured to tunnel traffic to the GSA edge.
All devices on the branch network go through GSA without needing the client installed.
Limitations vs full client:
  - No per-user identity -- traffic attributed to the branch, not individual user
  - No user-level Conditional Access enforcement
  - All branch traffic goes through GSA (no per-device selectivity)
Best for: shared/unmanaged devices, printers, IoT on the branch network.

Q5 -- Internet access content filtering
Path: Global Secure Access > Secure > Web content filtering policies > New policy.
Add rule: Category = [blocked category] > Action = Block.
Assign policy: Global Secure Access > Secure > Security profiles >
  create or edit profile > add the filtering policy > assign profile to user group.
Verify: Global Secure Access > Monitor > Traffic logs > filter by action = Blocked.
Test: user attempts to access a blocked site > should see block page.

Q6 -- Investigating bypassed restriction
Log type: Global Secure Access > Monitor > Traffic logs > filter Internet Access.
Look for: the user's UPN, the destination URL, timestamp matching the reported access.
If no log entry exists: user likely bypassed GSA by using a different network path.
Detection: check if GSA client was running at that time (client health logs),
check if user was on VPN or direct corporate network instead of GSA.
Enforcement: CA policy requiring GSA compliance -- "Require Global Secure Access
compliant network" condition blocks access from non-GSA network paths.
"""
    },

    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC2-004",
        "template_variant": "C",
        "domain": "2",
        "sub_topic": "Global Secure Access",
        "objective": "2.4 - Implement Global Secure Access",
        "scenario_template": """
{org_name} is planning a full Zero Trust network transformation, replacing
their {vpn_product} VPN and web proxy with Global Secure Access.

Migration scope:
  - {num_remote} remote workers currently on VPN
  - {num_branch} branch offices with site-to-site VPN
  - {num_apps} internal applications of varying sensitivity
  - Microsoft 365 and {saas_app} SaaS traffic currently proxied
  - Internet access currently filtered by {proxy_product} on-premises proxy

Questions:
1. Design the GSA migration in phases. What order do you migrate components
   (M365 traffic, internet access, private apps) and why? What is the
   recommended parallel running period before decommissioning the VPN?
2. Classify the {num_apps} internal applications into GSA Private Access
   segments. What criteria determine whether an app gets its own segment
   vs being grouped with others? What is the security benefit of
   per-application segments vs broad network segments?
3. Design the Conditional Access policy for GSA access. What is the
   "Compliant Network" CA condition and how does it enforce that users
   MUST go through GSA rather than direct internet access?
4. The {proxy_product} proxy currently enforces web filtering policies.
   Map the existing proxy categories to GSA Internet Access filtering policies.
   What categories and actions does GSA Internet Access support?
   What filtering is NOT available in GSA that requires a third-party solution?
5. After migration, design the ongoing GSA governance model. What metrics
   do you monitor, how do you handle connector scaling as user numbers grow,
   and what is the process for onboarding a new internal application to GSA?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Council", "Alpine Manufacturing"],
            "vpn_product": ["Cisco AnyConnect", "Palo Alto GlobalProtect", "Fortinet FortiClient", "Pulse Secure"],
            "num_remote": ["450", "1200", "89", "2400"],
            "num_branch": ["8", "23", "3", "45"],
            "num_apps": ["34", "12", "67", "8"],
            "saas_app": ["Salesforce", "ServiceNow", "Workday", "SAP SuccessFactors"],
            "proxy_product": ["Zscaler", "Bluecoat", "Cisco Umbrella", "Forcepoint"],
        },
        "exam_objectives": ["2.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC2-004-C: GSA Migration Planning

Q1 -- Phased migration order
Phase 1 -- Microsoft 365 traffic (lowest risk, highest benefit):
  Enable M365 traffic profile. Immediate latency improvement.
  No security risk -- M365 is already cloud, GSA just optimises the path.
  Parallel run: 2-4 weeks. Monitor: M365 performance metrics, sign-in success.

Phase 2 -- Internet Access (medium complexity):
  Enable Internet Access profile, configure web filtering policies.
  Replace proxy for internet-bound traffic.
  Parallel run: 4-8 weeks. Shadow mode: log but don't block initially.

Phase 3 -- Private Access (highest complexity, replaces VPN):
  Migrate apps one at a time, starting with non-critical.
  Parallel run: 8-12 weeks with both VPN and GSA available.
  Decommission VPN only after all apps migrated and users validated.
Recommended total parallel running period: 3-6 months before VPN decommission.

Q2 -- Application segment classification
Per-application segment (recommended for sensitive apps):
  - Contains sensitive data (payroll, patient records, financial)
  - Requires individual access control and audit trail
  - Different user populations need access (not all remote users)
  Security benefit: zero lateral movement -- users access only that app,
  not the network segment it sits on.
Grouped segments (acceptable for less sensitive):
  - Same user population needs all apps in the group
  - Apps share the same sensitivity level
  - Administrative overhead justifies grouping
Criteria: data sensitivity, user population, compliance requirements,
audit granularity needed.

Q3 -- Compliant Network CA condition
The "Compliant Network" condition in CA verifies the user is connecting
through Global Secure Access (either client or remote network connectivity).
Configure: CA policy > Conditions > Network > Compliant network = Yes.
Effect: sign-ins from outside GSA are blocked for covered applications.
This enforces that ALL access to private apps goes through GSA,
preventing users from bypassing GSA by connecting directly.
Important: ensure break-glass accounts are excluded from this policy.

Q4 -- Proxy to GSA filtering mapping
GSA Internet Access supports:
  Categories: adult content, gambling, social media, malware, phishing,
  botnets, streaming, personal storage, anonymisers.
  Actions: Allow, Block, Alert (log but allow).
What GSA does NOT currently support (may need third-party):
  - SSL inspection / HTTPS deep packet inspection (limited in GSA preview)
  - Advanced DLP for internet traffic
  - Custom category lists beyond Microsoft's built-in categories
  - ICAP integration for third-party content scanning
Migration approach: map existing proxy categories to GSA equivalents,
identify gaps, maintain proxy in parallel for features GSA cannot replace.

Q5 -- Ongoing GSA governance model
Metrics to monitor weekly:
  - Connector health (all connectors green)
  - Traffic volume per app segment (detect anomalies)
  - Block rate for internet filtering (too high = overly restrictive)
  - User connection failures (troubleshoot proactively)
Connector scaling: add connectors in the same connector group as load grows.
  GSA load balances across healthy connectors automatically.
  Rule of thumb: one connector per 500-1000 concurrent users.
Onboarding new internal app:
  1. Deploy connector in the target network segment
  2. Create new application segment (FQDN/IP/port)
  3. Assign appropriate user/group
  4. Create CA policy for the app (MFA, compliant device as required)
  5. Test with pilot group before broad rollout
  6. Update network firewall to allow connector outbound only
  7. Document in application inventory
"""
    },
]

# ════════════════════════════════════════════════════════════════════════════
# UPDATED DOMAIN2_SCENARIOS list
# Replace the existing DOMAIN2_SCENARIOS in sc300_module.py with this
# ════════════════════════════════════════════════════════════════════════════

DOMAIN2_SCENARIOS = SC2_001_TEMPLATES + SC2_002_TEMPLATES + SC2_003_TEMPLATES + SC2_004_TEMPLATES

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


SC4_001_TEMPLATES = [
 
    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC4-001",
        "template_variant": "A",
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
ANSWER GUIDE -- SC4-001-A: Privileged Identity Management (PIM)
 
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
 
Q6 -- PIM audit report
Path: PIM > Microsoft Entra roles > Audit history.
Filter: Date range = last 30 days, Activity = "Role activated."
Export: Download CSV from the audit history view.
"""
    },
 
    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC4-001",
        "template_variant": "B",
        "domain": "4",
        "sub_topic": "Privileged Identity Management (PIM)",
        "objective": "4.3 - Plan and implement privileged access",
        "scenario_template": """
A security review at {org_name} has flagged the following PIM misconfigurations:
 
  - {risky_role} can be self-activated with no approval and no time limit
  - {num_permanent_admins} users have active (not eligible) assignments to sensitive roles
  - PIM alerts are not configured -- activations happen silently
  - A third-party auditor needs read-only access to PIM audit logs
  - {num_devops} developers have permanent Contributor access to ALL Azure subscriptions
  - The "{pim_group}" group has 34 members but no-one knows who approved them
 
Questions:
1. {risky_role} has no approval requirement. Walk through configuring approval workflow
   in PIM. What is the difference between "approver" and "backup approver"?
   What happens if no approver responds within the configured timeframe?
2. Explain the difference between "Active assignment" and "Eligible assignment" in PIM.
   When would you use a permanent Active assignment legitimately?
3. Configure PIM alerts for your tenant. Name THREE built-in PIM alerts and
   what each detects. Where are alerts configured and how are notifications sent?
4. The third-party auditor needs PIM audit log access only. What is the minimum
   Entra role that grants this without any ability to modify PIM settings?
5. Design a PIM for Azure Resources structure for {num_devops} developers across
   {num_subscriptions} Azure subscriptions. How do you avoid configuring each
   subscription individually?
6. Investigate the "{pim_group}" group membership issue. What PIM report shows
   who approved each assignment and when? What action do you take for
   assignments with no approval record?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Alpine Engineering", "Pacific Council"],
            "risky_role": ["Privileged Role Administrator", "User Administrator", "Application Administrator", "Cloud Application Administrator"],
            "num_permanent_admins": ["12", "7", "19", "4"],
            "num_devops": ["8", "15", "4", "25"],
            "num_subscriptions": ["3", "6", "2", "8"],
            "pim_group": ["Security-Ops-Team", "Prod-Access-Group", "CloudOps-Admins", "DR-Response-Team"],
        },
        "exam_objectives": ["4.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-001-B: PIM Misconfigurations and Remediation
 
Q1 -- Approval workflow and backup approvers
Path: PIM > Microsoft Entra roles > [role] > Settings > Edit > Require approval.
Add primary approvers (named individuals or group).
Backup approver: receives the approval request if primary approver does not
respond within the configured time (default 24 hours).
If NO approver (primary or backup) responds: activation request EXPIRES and
is automatically DENIED. The requestor must submit a new request.
This is by design -- PIM defaults to deny on timeout, not approve.
 
Q2 -- Active vs Eligible assignment
Eligible assignment: user must activate the role (MFA, justification, approval)
before it takes effect. Role is dormant until activated.
Active assignment: role is permanently on -- no activation required.
Legitimate uses for permanent Active assignment:
  - Break-glass accounts (must work even if PIM is unavailable)
  - Service accounts that cannot perform interactive MFA
  - On-call security roles where instant access is safety-critical
For all other privileged roles: eligible assignment is the correct choice.
 
Q3 -- Built-in PIM alerts
Path: PIM > Microsoft Entra roles > Alerts.
Three key alerts:
  1. "Roles are being activated too frequently" -- detects potential abuse
     where the same user activates repeatedly in a short window
  2. "Potential stale accounts in a privileged role" -- flags accounts
     that have not signed in for 30+ days but hold eligible assignments
  3. "Roles don't require MFA for activation" -- compliance gap detection
Notifications: configure email recipients per alert in the alert settings.
Alerts also appear in the PIM dashboard and can feed into Sentinel via
Diagnostic Settings > AuditLogs.
 
Q4 -- Read-only PIM audit access
Minimum role: Security Reader
This role grants read access to PIM audit history, role assignments,
and activation history without any ability to modify settings or assignments.
Alternatively: Reports Reader (more limited -- audit logs only).
Do NOT assign Privileged Role Administrator -- that grants full PIM control.
 
Q5 -- PIM for Azure Resources at scale
Rather than configuring each subscription individually, use Management Groups.
Assign PIM eligible roles at the Management Group level -- assignments
inherit down to all child subscriptions automatically.
Path: PIM > Azure resources > Select management group (not individual subscription).
Add eligible assignment for Contributor to the developer group.
Scope: management group covers all subscriptions beneath it.
Activation settings: 4hr max, justification required, approval for production.
 
Q6 -- Investigating unauthorised group membership
Path: PIM > Groups > [pim_group] > Audit history.
Filter: Activity = "Add member to group" -- shows who was added, when, and
which admin approved or whether it was a direct assignment bypassing PIM.
Assignments with no PIM approval record were added directly (bypassing PIM).
Action: remove those assignments > re-add via PIM eligible assignment >
configure PIM for the group if not already enabled to prevent future bypass.
"""
    },
 
    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC4-001",
        "template_variant": "C",
        "domain": "4",
        "sub_topic": "Privileged Identity Management (PIM)",
        "objective": "4.3 - Plan and implement privileged access",
        "scenario_template": """
{org_name} is preparing for an ISO 27001 audit. The auditor has requested
evidence of privileged access controls. Current findings:
 
  - No evidence that privileged role activations are being reviewed
  - {num_admins} Global Admins -- auditor says maximum should be 4
  - Break-glass accounts cannot be tested without triggering real alerts
  - A recent incident: {incident_description}
  - PIM access reviews have never been configured
  - Privileged access workstation (PAW) policy does not exist
 
Questions:
1. The auditor wants evidence of privileged access review. Configure a
   PIM Access Review specifically for Global Administrator role members.
   How does a PIM access review differ from a standard group access review?
2. Reduce Global Admins from {num_admins} to 4 using PIM. Walk through
   the process of identifying which admins to convert and which roles to
   use instead (list at least 4 alternative roles and their use cases).
3. Design a break-glass account testing procedure that can be run quarterly
   WITHOUT triggering real security alerts. What steps are involved and
   what evidence do you retain for the auditor?
4. {incident_description}. Perform a post-incident PIM review. What specific
   PIM reports and logs would you pull? What settings would you tighten?
5. Define a Privileged Access Workstation (PAW) policy for your Global Admins.
   What Conditional Access policy enforces that admin roles can only be
   activated from compliant, dedicated devices?
6. The auditor asks for a complete export of all privileged role assignments
   (active and eligible) across Entra ID and Azure resources. How do you
   produce this report and what format does it export in?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Insurance", "Alpine Council"],
            "num_admins": ["11", "18", "7", "24"],
            "incident_description": [
                "a Global Admin account was activated at 2am from an unknown location",
                "a Privileged Role Administrator assigned themselves Owner on the production subscription",
                "an Exchange Admin exported the entire mailbox of the CEO without authorisation",
                "a contractor account was found with Security Administrator role active for 6 months after contract end",
            ],
        },
        "exam_objectives": ["4.3"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-001-C: PIM for Audit and Compliance
 
Q1 -- PIM Access Review for Global Administrator
Path: Identity Governance > Access Reviews > New access review >
Microsoft Entra roles > Global Administrator.
Differences from standard group access review:
  - Can target eligible assignments, active assignments, or both separately
  - Reviewers see PIM activation history alongside the assignment (context)
  - Auto-apply can remove eligible assignments (not just group membership)
  - Results feed directly into PIM assignment records and audit trail
  - Recommended reviewer: Privileged Role Administrator or CISO, never self-review
 
Q2 -- Reducing Global Admin count
Process: PIM > Microsoft Entra roles > Global Administrator > Assignments.
Review each admin: what do they actually use GA for?
Common replacements:
  - Password resets -> Authentication Administrator
  - Licence management -> Licence Administrator
  - Exchange management -> Exchange Administrator
  - Conditional Access -> Security Administrator
  - User management -> User Administrator
  - Billing -> Billing Administrator
Keep 2 permanent break-glass + 2 eligible GA for genuine GA tasks.
Remove all others and assign scoped roles instead.
 
Q3 -- Break-glass testing procedure (without triggering alerts)
Step 1: Notify the security team and SOC IN ADVANCE (scheduled test).
Step 2: Document the test in the change management system.
Step 3: Sign in with break-glass account from a known, controlled location.
Step 4: Verify sign-in succeeds and MFA (FIDO2) works correctly.
Step 5: Immediately sign out -- do not perform any admin actions.
Step 6: Verify alert fired in Sentinel -- confirm monitoring is working.
Step 7: Document: date tested, tester, result, alert confirmed.
Step 8: Rotate the password/verify FIDO2 key is still in physical safe.
The PRE-NOTIFICATION is what prevents a real incident response being triggered.
Retain the test documentation as audit evidence.
 
Q4 -- Post-incident PIM review
Reports to pull:
  - PIM > Audit history: filter by the compromised/misused account
  - Sign-in logs: all sign-ins for the account in the 30 days prior
  - PIM > Role settings: confirm approval was required (was it bypassed?)
Settings to tighten after incident:
  - Reduce maximum activation duration
  - Add additional approvers
  - Enable require justification if not already on
  - Review and remove any permanent active assignments in the affected role
  - Enable Sentinel alert for the specific role if not already configured
 
Q5 -- PAW policy via Conditional Access
Create a dedicated device group: "PAW-Devices" in Entra ID.
Enrol PAW devices in Intune with hardened compliance policy.
CA policy: Assignments = Directory roles (all admin roles) >
Conditions: Filter for devices = device is NOT in "PAW-Devices" group >
Grant: Block access.
Effect: admin roles can ONLY be activated from PAW devices.
Complement with: named location restriction (corporate network only for PAW).
 
Q6 -- Full privileged role assignment export
Entra ID roles: PIM > Microsoft Entra roles > Assignments > Download (CSV).
Includes: role name, member, assignment type (active/eligible), start/end date.
Azure resource roles: PIM > Azure resources > each scope > Assignments > Download.
For a combined report: use Microsoft Graph API or PowerShell:
  Get-MgRoleManagementDirectoryRoleAssignment (Entra roles)
  Get-AzRoleAssignment (Azure RBAC roles)
Export format: CSV, suitable for spreadsheet review by auditor.
"""
    },
]
 
# ════════════════════════════════════════════════════════════════════════════
# SC4-002: Access Reviews — 3 templates
# ════════════════════════════════════════════════════════════════════════════
 
SC4_002_TEMPLATES = [
 
    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC4-002",
        "template_variant": "A",
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
ANSWER GUIDE -- SC4-002-A: Access Reviews
 
Q1 -- Access Review for sensitive group
Path: Entra admin centre > Identity Governance > Access Reviews > New access review.
  - Review type: Teams + Groups > select the sensitive group
  - Recurrence: chosen frequency
  - Reviewers: Selected reviewers -- choose the data owner or line manager
Do NOT use self-review for sensitive data.
For sensitive data always use a named manager, data owner, or security reviewer.
 
Q2 -- Privileged role access review
Path: Access Reviews > New access review > Microsoft Entra roles.
Key differences:
  - Scope can target only active or only eligible PIM assignments (or both)
  - Results can auto-remove eligible assignments if denied (PIM integration)
  - Review scope = specific privileged roles, not group membership
  - Recommended reviewer: senior security team member
 
Q3 -- No-response setting
For a sensitive group: set to "Remove access."
Rationale: if a reviewer cannot confirm access is still needed,
access defaults to denied (least privilege principle).
 
Q4 -- Guest-specific review with auto-removal
Configure: scope = Guest users only.
Enable: Auto apply results to resource = Yes.
Enable: If reviewer doesn't respond = Remove access.
Enable: Action on denied guest users = Remove user's membership from the group
AND disable sign-in.
 
Q5 -- Lifecycle Workflow for offboarding
Path: Identity Governance > Lifecycle Workflows > New workflow.
Trigger: "Employee leave" (fires when employeeLeaveDateTime is set).
Tasks: Disable account, remove group memberships, remove Teams,
send notification to manager, transfer OneDrive to manager.
"""
    },
 
    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC4-002",
        "template_variant": "B",
        "domain": "4",
        "sub_topic": "Access Reviews",
        "objective": "4.2 - Plan, implement, and manage access reviews in Microsoft Entra",
        "scenario_template": """
{org_name} has {num_apps} enterprise applications and wants to implement
a comprehensive access review programme from scratch.
 
Current problems:
  - Application owners do not know who has access to their apps
  - {num_service_accounts} service accounts have never been reviewed
  - A recently departed employee ({departed_employee}) still has an active
    guest account with access to {sensitive_app}
  - Access Reviews have been created but results are never applied
  - {num_dynamic_group} dynamic groups control app access -- membership is never audited
 
Questions:
1. Design a quarterly access review programme covering: users, guests, privileged roles,
   and service accounts. What review scope and reviewer type suits each category?
2. The departed guest {departed_employee} still has access. Walk through manually
   revoking their access immediately and then preventing this recurring automatically.
   What two Entra features work together to solve this?
3. Access Review results are being created but never applied. What setting ensures
   results are automatically applied when the review period ends?
   What is the risk of NOT auto-applying?
4. Configure an Access Review for the {num_apps} enterprise applications.
   What review type do you select? Who should review app access --
   the app owner, the user's manager, or the user themselves?
5. Service accounts cannot do self-review and have no manager. How do you
   review {num_service_accounts} service account assignments? 
   What is the recommended long-term solution for service account access?
""",
        "variables": {
            "org_name": ["Northwind Finance", "Contoso Health", "Pacific Engineering", "Alpine Council"],
            "num_apps": ["18", "34", "8", "52"],
            "num_service_accounts": ["12", "28", "7", "45"],
            "departed_employee": ["j.smith@partnerorg.com", "contractor@vendor.com", "consultant@external.co.nz", "temp@agency.com"],
            "sensitive_app": ["Finance ERP", "Patient Records System", "HR Payroll Portal", "Legal Case Management"],
            "num_dynamic_group": ["14", "6", "22", "9"],
        },
        "exam_objectives": ["4.2"],
        "difficulty": "intermediate",
        "answers": """
ANSWER GUIDE -- SC4-002-B: Comprehensive Access Review Programme
 
Q1 -- Access review programme design
Users (internal): quarterly, reviewer = user's manager, scope = group membership
  or app role assignments. Manager has context on whether access is still needed.
Guests (external): monthly or quarterly, reviewer = sponsor (internal user who
  invited them), auto-remove on no response.
Privileged roles: monthly, reviewer = Privileged Role Administrator or CISO,
  scope = both active and eligible PIM assignments.
Service accounts: quarterly, reviewer = nominated IT owner (not self-review),
  scope = group memberships and app role assignments.
 
Q2 -- Revoking departed guest immediately + preventing recurrence
Immediate revocation:
  Entra > Users > [guest account] > Revoke sessions > then Disable account.
  Remove from all groups manually if access review is not yet configured.
Preventing recurrence -- two features working together:
  1. Access Reviews with auto-apply: catches guests who slip through offboarding
  2. Lifecycle Workflows with "Guest cleanup" task: automatically removes
     guest accounts after a configurable period of inactivity.
Set guest account expiry policy: External Identities > Settings >
Guest user access expiry = enabled with a defined expiry period.
 
Q3 -- Auto-apply access review results
Setting: Access Reviews > [review] > Settings > "Auto apply results to resource" = Yes.
Also set: "If reviewers don't respond" = Remove access (for sensitive resources).
Risk of NOT auto-applying: review results are advisory only. Without auto-apply,
a reviewer can deny access but the user keeps it until an admin manually
processes each result -- which often never happens (review fatigue).
 
Q4 -- Enterprise application access review
Path: Access Reviews > New > Applications (not Teams + Groups).
Select: specific enterprise applications or all apps.
Reviewer recommendation: Application owner for business apps (they know
who legitimately needs access). Manager for productivity apps.
Self-review is acceptable ONLY for low-sensitivity applications.
For high-sensitivity apps (ERP, HR, patient data): always use a named reviewer.
 
Q5 -- Service account access review
Reviewer: assign a named IT owner as the designated reviewer for each
service account. Document the owner in a custom security attribute
or extension attribute on the service account object.
Path: Access Reviews > New > select service account group > 
Reviewers = Selected reviewers > add the IT owner.
Long-term solution: replace service accounts with Managed Identities
(no credentials to manage, no licence required, automatically scoped).
Service accounts that cannot be replaced: review quarterly, enforce
named ownership, restrict to named IP locations via CA policy.
"""
    },
 
    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC4-002",
        "template_variant": "C",
        "domain": "4",
        "sub_topic": "Access Reviews",
        "objective": "4.2 - Plan, implement, and manage access reviews in Microsoft Entra",
        "scenario_template": """
{org_name} has deployed Lifecycle Workflows to automate identity governance
but is experiencing the following issues:
 
  - Joiner workflow runs but new starters do not have access on day one
  - Leaver workflow is not triggered reliably -- {leaver_issue}
  - {num_stale} accounts are 120+ days stale and were not caught by reviews
  - A mover scenario (promotion to manager) is not handled -- {mover_issue}
  - Access Reviews for {sensitive_group} are running but 60% of reviewers
    never complete them
 
Questions:
1. The joiner workflow fires but access is not ready on day one. Diagnose
   the likely cause. What is the recommended trigger offset (days before
   start date) for joiner workflows and why?
2. {leaver_issue}. Fix the leaver workflow trigger. What attribute must the
   HR system write to Entra ID to trigger the "Employee leave" workflow?
   What happens if this attribute is never set?
3. Design a mover workflow for a promotion from {source_role} to {target_role}.
   What tasks would it include beyond a standard joiner workflow?
   How do you prevent the employee retaining their old access?
4. {num_stale} accounts were not caught. Review your stale account strategy.
   What Lifecycle Workflow task automatically disables accounts inactive for
   a configurable number of days? What is the trigger type?
5. 60% of reviewers for {sensitive_group} are not completing reviews.
   What three escalation mechanisms does Microsoft Entra provide?
   If you switch to "Manager as reviewer" what happens when a user has
   no manager assigned?
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Finance", "Pacific Council", "Northwind Manufacturing"],
            "leaver_issue": [
                "the HR system updates AD but employeeLeaveDateTime is never written to Entra ID",
                "the workflow is configured but the trigger offset is set to 0 days -- it fires too late",
                "the leaver workflow only runs on weekdays -- employees terminating on Friday are missed until Monday",
            ],
            "num_stale": ["34", "89", "17", "156"],
            "sensitive_group": ["Finance-FullAccess", "PatientRecords-Admins", "ExecutiveDocuments-Access", "PayrollSystem-Users"],
            "mover_issue": [
                "the employee retains all previous group memberships after promotion",
                "the new manager role requires PIM activation but the workflow does not handle PIM",
                "the mover workflow removes old access but new access takes 48 hours to propagate",
            ],
            "source_role": ["Senior Analyst", "Ward Nurse", "Finance Officer", "IT Technician"],
            "target_role": ["Team Manager", "Charge Nurse", "Finance Manager", "IT Team Lead"],
        },
        "exam_objectives": ["4.2"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-002-C: Lifecycle Workflows Troubleshooting
 
Q1 -- Joiner workflow day-one access issue
Most likely cause: the workflow trigger is set to 0 days before start date
(fires ON the start date) but provisioning tasks (group assignment, licence,
access package) take time to process and replicate.
Recommended offset: set trigger to 1-2 days BEFORE employeeHireDate.
Path: Lifecycle Workflows > [workflow] > Basics > Days before/after event = -2.
This gives time for: group membership to process, licence to assign,
access package auto-assignment to complete, and MFA registration email to send.
 
Q2 -- Leaver workflow trigger fix
The "Employee leave" trigger fires on the employeeLeaveDateTime attribute.
This attribute must be written to the Entra ID user object -- it does NOT
sync automatically from AD unless specifically mapped in Entra Connect.
Fix: configure Entra Connect attribute mapping to sync employeeLeaveDateTime
from AD extension attribute, OR have the HR system write it directly via
Microsoft Graph API (PATCH /users/{id} with employeeLeaveDateTime).
If attribute is never set: the workflow never fires -- manual offboarding
remains the fallback, which is the current failure mode.
 
Q3 -- Mover workflow for promotion
Tasks beyond standard joiner:
  1. Remove user from old department security groups
  2. Remove old access package assignment
  3. Assign new access package (manager-level)
  4. Update manager attribute (so future access reviews route correctly)
  5. Send notification to old manager and new skip-level manager
  6. (If PIM): add eligible assignment to management role
Preventing old access retention: configure the workflow to explicitly
REMOVE previous group memberships before assigning new ones. Without this
step users accumulate access across every role they have ever held
(privilege creep -- a common audit finding).
 
Q4 -- Stale account handling via Lifecycle Workflows
Task: "Disable user account" triggered by inactivity.
Trigger type: "Attribute-based" -- trigger on lastSignInDateTime
being older than a configurable threshold (e.g. 90 days).
Path: Lifecycle Workflows > New workflow > Trigger = Attribute changes >
configure lastSignInDateTime condition.
Note: lastSignInDateTime is only available with Entra ID P1 or higher.
Complement with: Access Reviews set to auto-disable on no sign-in.
 
Q5 -- Escalating incomplete access reviews
Three Entra escalation mechanisms:
  1. Email reminders: configured in Access Review settings -- send reminders
     at configurable intervals before the deadline
  2. Escalation reviewers: a secondary reviewer receives the request if the
     primary reviewer does not respond within a set number of days
  3. Auto-apply with "Remove access" on no response: ensures inaction
     has a consequence rather than silently preserving access
If "Manager as reviewer" and user has no manager assigned:
  The review falls back to the configured fallback reviewer
  (set in Access Review settings > "Fallback reviewers").
  If no fallback is configured: the review item is left incomplete.
  Always configure a fallback reviewer for manager-based reviews.
"""
    },
]
 
# ════════════════════════════════════════════════════════════════════════════
# SC4-003: Entitlement Management — 3 templates
# ════════════════════════════════════════════════════════════════════════════
 
SC4_003_TEMPLATES = [
 
    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC4-003",
        "template_variant": "A",
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
ANSWER GUIDE -- SC4-003-A: Entitlement Management
 
Q1 -- Catalog vs Access Package
Catalog: container grouping related resources, defines who can manage them.
Access Package: bundle of specific resources users can request or be auto-assigned.
Catalog owner: department head or IT lead.
Access Package manager: IT admin or HR.
 
Q2 -- Access Package with auto-assignment
Path: Identity Governance > Entitlement Management > Access packages > New.
Policy 1 (auto-assignment): rule (user.department -eq "Finance").
Policy 2 (self-service): require manager approval.
Lifecycle: expiration after chosen days, require renewal = Yes.
 
Q3 -- External access package
Prerequisite: Connected organizations > New > add partner by domain/tenant ID.
Access Package > Requests > Users not in your directory > select org.
Set hard expiry -- no renewal for external contractors.
 
Q4 -- Terms of Use
Format: PDF only.
Enforcement: via Conditional Access policy targeting the app.
Create ToU in Identity Governance > Terms of use > New terms.
CA policy: Grant = Require terms of use.
 
Q5 -- Reporting and expiry
Report: Identity Governance > Entitlement Management > Reports > Access package assignments.
On expiry without renewal: user automatically removed from all resources in the package.
"""
    },
 
    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC4-003",
        "template_variant": "B",
        "domain": "4",
        "sub_topic": "Entitlement Management and Access Packages",
        "objective": "4.1 - Plan and implement entitlement management in Microsoft Entra",
        "scenario_template": """
{org_name} has implemented Entitlement Management but is experiencing problems:
 
  - External users from {partner_org} cannot request access packages
  - An access package for {department} was created but auto-assignment is not working
  - {num_orphaned} access package assignments have no active policy (orphaned)
  - The approval workflow takes {approval_days} days -- requestors are frustrated
  - Access packages contain resources from multiple catalogs -- causing errors
 
Questions:
1. {partner_org} users cannot request the external access package. Diagnose
   the three most likely causes. Walk through verifying each one in the portal.
2. The {department} auto-assignment policy is not working. What is the most common
   cause of auto-assignment rules failing? How do you test an auto-assignment
   rule before enabling it for all users?
3. Explain what an "orphaned assignment" is in Entitlement Management.
   How do you identify and remediate {num_orphaned} orphaned assignments?
4. The approval workflow takes {approval_days} days. What settings can you
   change to speed up approvals without removing the approval requirement?
   What is the maximum number of approval stages in an access package policy?
5. An access package cannot contain resources from multiple catalogs. Redesign
   the {department} access package so all required resources are in one catalog.
   What is the process for moving a resource from one catalog to another?
""",
        "variables": {
            "org_name": ["Contoso Health", "Fabrikam Finance", "Northwind Engineering", "Pacific Council"],
            "partner_org": ["Southern Cross Partners", "Alpine Consulting", "Bay Advisory Group", "Pacific Rim Solutions"],
            "department": ["Finance", "Clinical", "Legal", "Engineering"],
            "num_orphaned": ["23", "8", "45", "12"],
            "approval_days": ["5", "7", "10", "3"],
        },
        "exam_objectives": ["4.1"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-003-B: Entitlement Management Troubleshooting
 
Q1 -- External users cannot request access package
Three most likely causes:
  1. Connected organization not configured or in "Proposed" state (not "Configured"):
     Path: Identity Governance > Entitlement Management > Connected organizations.
     Verify partner org is listed and State = Configured (not Proposed).
  2. Access package policy does not allow external users:
     Access package > Policies > check "Who can request" -- must include
     "Users not in your directory" or the specific connected organization.
  3. External collaboration settings blocking B2B invitations:
     Entra > External Identities > External collaboration settings >
     verify the partner domain is not on the blocklist and invitations are allowed.
 
Q2 -- Auto-assignment rule not working
Most common cause: the attribute used in the rule does not match the actual
user attribute value. Example: rule uses (user.department -eq "Finance") but
the user's department attribute is "finance" (lowercase) or "FINANCE" or blank.
Rules are case-sensitive in some contexts.
Testing before enabling: Access package > Policies > Auto-assignment policy >
"Evaluate" -- enter a specific user's UPN to see if they match the rule.
Also check: the attribute is populated on the user object (many tenants have
blank department attributes because HR sync is not configured).
 
Q3 -- Orphaned assignments
An orphaned assignment exists when an access package assignment has no
active policy -- the policy was deleted after the assignment was created.
The user retains access but the assignment cannot be renewed or managed normally.
Identify: Identity Governance > Entitlement Management > Reports >
Access package assignments > filter by "Policy" = blank/none.
Remediate: either recreate the policy and link the assignments, or remove
the orphaned assignments manually and ask affected users to re-request.
 
Q4 -- Speeding up approval workflow
Settings to adjust:
  - Approval timeout: reduce from default (14 days) to 2-3 days
  - Add backup approvers: if primary approver doesn't respond within
    X days, request escalates to backup automatically
  - Enable email notifications with direct approve/deny links
    (approvers can approve from email without signing into the portal)
  - Reduce approval stages: maximum is 2 stages in an access package policy.
    If 2-stage approval is causing the delay, consider whether both stages
    are genuinely necessary for the sensitivity of the resource.
 
Q5 -- Resource from multiple catalogs
Resources in an access package must all belong to the SAME catalog.
Process to move a resource to the correct catalog:
  1. Remove the resource from its current catalog
     (Catalog > Resources > remove -- does NOT delete the resource itself)
  2. Add the resource to the target catalog
     (Target catalog > Resources > Add resource)
  3. Update all access packages in the target catalog to reference the resource.
Note: removing a resource from a catalog removes it from ALL access packages
in that catalog -- plan the move carefully and notify affected package managers.
"""
    },
 
    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC4-003",
        "template_variant": "C",
        "domain": "4",
        "sub_topic": "Entitlement Management and Access Packages",
        "objective": "4.1 - Plan and implement entitlement management in Microsoft Entra",
        "scenario_template": """
{org_name} is onboarding {num_new_staff} new {staff_type} staff over the next
{onboard_period} weeks. The identity team must design a scalable access
provisioning model.
 
Current challenges:
  - New starters wait an average of {wait_days} days for access
  - {num_roles} different role profiles exist across {num_departments} departments
  - Some resources require manager approval; others can be self-service
  - Locums and agency staff need access for exactly {temp_duration} days
  - The CISO requires that all access to {sensitive_app} is justified and auditable
 
Questions:
1. Design a scalable access package architecture for {num_roles} role profiles
   across {num_departments} departments. How many catalogs would you create
   and why? What naming convention would you recommend?
2. Reduce the {wait_days}-day wait to day-one access using auto-assignment.
   What HR attribute must be consistently populated for auto-assignment to work?
   What is the risk of relying solely on auto-assignment without a self-service
   request option?
3. Design the approval policy matrix: which resource types require manager
   approval, which require IT approval, and which can be self-service?
   Justify each decision with a security principle.
4. Configure time-limited access packages for locums/agency staff lasting
   exactly {temp_duration} days with no renewal option. What prevents a
   manager from manually extending the assignment beyond {temp_duration} days?
5. The CISO requires full auditability for {sensitive_app} access.
   Design the complete governance chain: access package approval, Terms of Use,
   Access Review, and expiry. How do you produce a single audit report
   showing the full lifecycle of a user's access to {sensitive_app}?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Council", "Pacific Insurance", "Alpine Manufacturing"],
            "num_new_staff": ["45", "120", "18", "200"],
            "staff_type": ["clinical", "administrative", "engineering", "finance"],
            "onboard_period": ["4", "8", "12", "6"],
            "wait_days": ["3", "7", "5", "10"],
            "num_roles": ["8", "15", "6", "22"],
            "num_departments": ["4", "8", "3", "12"],
            "temp_duration": ["30", "60", "90"],
            "sensitive_app": ["Patient Records System", "Finance ERP", "HR Payroll Portal", "Legal Case Management"],
        },
        "exam_objectives": ["4.1"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-003-C: Scalable Entitlement Management Design
 
Q1 -- Catalog architecture for multiple departments
Recommended: one catalog per department or business unit.
Rationale: catalog ownership maps to department heads who know their resources.
Cross-department resources (shared SharePoint, common Teams channels) go in
a shared "Common Resources" catalog managed by IT.
Naming convention: [ORG]-[DEPT]-Catalog (e.g. CONTOSO-FINANCE-Catalog).
Access packages: [DEPT]-[ROLE]-[LEVEL] (e.g. FINANCE-Analyst-Standard).
Consistent naming enables reporting and reduces confusion as the catalogue grows.
 
Q2 -- Auto-assignment for day-one access
Required HR attribute: department (or jobTitle, or employeeType).
The attribute must be written to Entra ID BEFORE the start date --
ideally via SCIM provisioning from the HR system on day minus 1.
Risk of auto-assignment only (no self-service option):
  If a user's attribute is wrong or missing, they get no access and
  there is no way for them to request it themselves -- they must contact IT.
Best practice: auto-assignment as the primary mechanism + self-service
request as a fallback for attribute mismatches.
 
Q3 -- Approval policy matrix
Self-service (no approval): low-sensitivity productivity tools
  (Teams channels, SharePoint team sites, training platforms).
  Principle: availability -- friction should match sensitivity.
Manager approval: standard business applications (ERP read-only,
  department SharePoint, standard M365 groups).
  Principle: manager has business context for whether access is needed.
IT/Security approval: privileged or sensitive applications (ERP write,
  patient records, financial systems, admin tools).
  Principle: technical review required alongside business justification.
Dual approval (manager + IT): highest sensitivity (payroll, clinical prescribing).
  Principle: separation of duties for critical resources.
 
Q4 -- Time-limited access with no renewal
Configure: Access package > Policies > Expiration > After number of days = chosen duration.
Set: "Allow requestors to extend access" = No.
Set: "Renewal allowed" = No.
What prevents manual extension: the policy hard-codes the expiry -- even an
admin cannot extend an assignment beyond the policy maximum without creating
a new assignment under a different policy.
For locums: create a dedicated "Temporary Staff" policy within the access package
with the hard expiry. Do NOT give locums the standard employee policy.
 
Q5 -- Full audit chain for sensitive app
1. Access Package approval: manager + IT approval required, justification field mandatory.
   Audit: Identity Governance > Entitlement Management > Requests report.
2. Terms of Use: PDF policy accepted at first sign-in via CA policy.
   Audit: Identity Governance > Terms of use > [policy] > Acceptances report.
3. Access Review: quarterly, selected reviewer (data owner), auto-remove on denial.
   Audit: Identity Governance > Access Reviews > [review] > Results report.
4. Expiry: assignment expires after policy period, user removed from app automatically.
   Audit: Entitlement Management > Assignments report (shows end date and removal).
Single audit report: combine all four reports using Microsoft Graph API or
export each to CSV and merge in Excel -- there is no single built-in report
that spans the full lifecycle, but the combination covers the complete chain.
"""
    },
]
 
# ════════════════════════════════════════════════════════════════════════════
# SC4-004: Identity Monitoring, Logs, and Reporting — 3 templates
# ════════════════════════════════════════════════════════════════════════════
 
SC4_004_TEMPLATES = [
 
    # ── Template A (original) ────────────────────────────────────────────────
    {
        "id": "SC4-004",
        "template_variant": "A",
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
ANSWER GUIDE -- SC4-004-A: Identity Monitoring
 
Q1 -- Diagnostic Settings
Path: Entra admin centre > Monitoring > Diagnostic settings > Add.
Categories: SignInLogs, NonInteractiveUserSignInLogs, ServicePrincipalSignInLogs,
AuditLogs, RiskyUsers, UserRiskEvents, ManagedIdentitySignInLogs.
Log Analytics: queryable with KQL, integrates with Sentinel, higher cost.
Storage Account: cheapest archival, not queryable in real time.
Best practice: both.
 
Q2 -- KQL multi-country detection
SignInLogs
| where ResultType == 0
| extend Country = tostring(LocationDetails.countryOrRegion)
| summarize Countries = dcount(Country), CountryList = make_set(Country)
    by UserPrincipalName, bin(TimeGenerated, 24h)
| where Countries >= [geo_count]
| project TimeGenerated, UserPrincipalName, Countries, CountryList
| order by Countries desc
 
Q3 -- Built-in Workbooks
a) Legacy auth: "Sign-ins using legacy authentication"
b) CA impact: "Conditional Access Insights and Reporting"
c) Risky sign-ins: "Microsoft Entra ID Protection" workbook
 
Q4 -- Secure Score actions
MFA for admins: CA policy targeting directory roles, Grant = Require MFA.
SSPR: Entra > Security > Password reset > All.
No password expiry: Entra > Users > Password expiration policy > Never expire.
 
Q5 -- Compromise investigation
Users > [user] > Sign-in logs > filter all statuses > look for unusual IP,
location, device, timing. Click suspicious event > CA tab, risk level.
Users > [user] > Audit logs > look for new MFA methods, role assignments,
app consent grants. If compromised: revoke sessions, reset password,
remove new MFA methods, check OAuth consent grants.
"""
    },
 
    # ── Template B ───────────────────────────────────────────────────────────
    {
        "id": "SC4-004",
        "template_variant": "B",
        "domain": "4",
        "sub_topic": "Identity Monitoring, Logs, and Reporting",
        "objective": "4.4 - Monitor identity activity by using logs, workbooks, and reports",
        "scenario_template": """
{org_name} has connected Microsoft Sentinel to Entra ID and wants to build
a comprehensive identity threat detection capability.
 
Current state:
  - Diagnostic settings configured -- SignInLogs and AuditLogs flowing to Sentinel
  - No custom KQL detection rules created yet
  - {num_false_positives} false positive alerts per week from built-in rules
  - A real incident was missed last month: {missed_incident}
  - The security team wants a single identity health dashboard
  - Workload identity (service principal) sign-ins are NOT being logged
 
Questions:
1. Write KQL queries for these two scenarios:
   a) Detect a user who fails MFA {mfa_fail_threshold} or more times within 1 hour
      (potential MFA fatigue attack)
   b) Detect a service principal signing in from an IP outside its known range
      (potential service principal hijack)
2. {missed_incident}. Explain why this was missed and what detection rule
   would have caught it. Write the KQL query.
3. You have {num_false_positives} false positives per week. Describe three
   techniques to tune KQL detection rules and reduce false positive rate
   without missing real threats.
4. Add service principal sign-in logs to your Diagnostic Settings.
   What log category covers this? Write a KQL query that shows the top 10
   service principals by sign-in volume in the last 7 days.
5. Design a single identity health dashboard in Azure Workbooks covering:
   MFA coverage, risky users, stale accounts, CA policy gaps, and
   legacy authentication usage. What data sources does each panel need?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Finance", "Alpine Engineering", "Pacific Gov"],
            "num_false_positives": ["45", "120", "18", "67"],
            "missed_incident": [
                "a Global Admin activated their role at 3am on a Sunday and exported all users -- no alert fired",
                "a service principal called the Graph API 10,000 times in one hour exfiltrating user data",
                "a contractor account signed in from 4 countries in 2 hours -- ID Protection did not flag it",
                "an attacker registered a new MFA method on a compromised account -- no alert was generated",
            ],
            "mfa_fail_threshold": ["5", "10", "3"],
        },
        "exam_objectives": ["4.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-004-B: Sentinel KQL and Identity Threat Detection
 
Q1a -- MFA fatigue detection KQL
SignInLogs
| where ResultType == 50074 or ResultType == 50076
    // MFA required errors -- user presented password but MFA failed/denied
| summarize FailCount = count() by UserPrincipalName, bin(TimeGenerated, 1h)
| where FailCount >= [threshold]
| project TimeGenerated, UserPrincipalName, FailCount
| order by FailCount desc
 
Q1b -- Service principal unusual IP KQL
// Requires known IP list stored as a watchlist named "ApprovedSPIPs"
ServicePrincipalSignInLogs
| where ResultType == 0
| join kind=leftanti (
    _GetWatchlist('ApprovedSPIPs') | project SearchKey
  ) on $left.IPAddress == $right.SearchKey
| project TimeGenerated, ServicePrincipalName, IPAddress, ResourceDisplayName
| order by TimeGenerated desc
 
Q2 -- Why the incident was missed + detection rule
Common reasons incidents are missed:
  - The relevant log category was not in Diagnostic Settings
  - The built-in analytic rule was disabled or not deployed
  - The event volume was below the alert threshold
Example rule for 3am admin activation:
AuditLogs
| where OperationName == "Add member to role"
| where hourofday(TimeGenerated) between (0 .. 5)
| where TargetResources contains "Global Administrator"
| project TimeGenerated, InitiatedBy, TargetResources
 
Q3 -- Reducing false positives
1. Allowlisting: add known safe IPs, users, and service accounts to
   watchlists and exclude them from detection rules using leftanti joins.
2. Threshold tuning: increase the count/frequency thresholds so only
   genuinely anomalous volumes trigger alerts (requires baseline analysis).
3. Entity behaviour baseline: use Sentinel's UEBA (User and Entity Behaviour
   Analytics) to compare against each user's own baseline rather than a
   global threshold -- reduces alerts for users who legitimately travel.
 
Q4 -- Service principal logging
Log category: ServicePrincipalSignInLogs (add to Diagnostic Settings).
Top 10 SPs by volume KQL:
ServicePrincipalSignInLogs
| where TimeGenerated > ago(7d)
| summarize SignInCount = count() by ServicePrincipalName
| top 10 by SignInCount desc
| project ServicePrincipalName, SignInCount
 
Q5 -- Identity health dashboard panels
MFA coverage: SignInLogs -- users signing in without MFA claim.
  Data source: SignInLogs in Log Analytics.
Risky users: RiskyUsers table -- current risk level and state.
  Data source: RiskyUsers (requires ID Protection P2).
Stale accounts: AuditLogs + SignInLogs -- last sign-in > 90 days.
  Data source: SignInLogs summarised by UserPrincipalName.
CA policy gaps: SignInLogs -- sign-ins where no CA policy applied.
  Data source: SignInLogs, filter ConditionalAccessStatus = notApplied.
Legacy auth: SignInLogs -- ClientAppUsed field contains legacy protocol names.
  Data source: SignInLogs filter ClientAppUsed in legacy protocol list.
"""
    },
 
    # ── Template C ───────────────────────────────────────────────────────────
    {
        "id": "SC4-004",
        "template_variant": "C",
        "domain": "4",
        "sub_topic": "Identity Monitoring, Logs, and Reporting",
        "objective": "4.4 - Monitor identity activity by using logs, workbooks, and reports",
        "scenario_template": """
{org_name} is preparing for a regulatory audit requiring evidence of
identity monitoring controls. The auditor has requested:
 
  - Evidence that privileged access is monitored in real time
  - Proof that legacy authentication has been eliminated
  - A report showing Identity Secure Score trend over {score_period} months
  - Evidence that all sign-in logs are retained for {retention_requirement} months
  - Demonstration that unusual sign-in activity triggers automated response
 
Current gaps:
  - Secure Score has dropped from {old_score} to {new_score} in 30 days
  - Log retention is only {current_retention} days
  - Automated response to risky sign-ins is not configured
 
Questions:
1. The auditor wants real-time privileged access monitoring. Configure
   three specific alerts in Sentinel or Log Analytics that cover:
   break-glass account usage, PIM activation outside business hours,
   and new role assignment to a guest user.
2. Prove legacy authentication has been eliminated. Which specific Workbook
   shows this? What does a "clean" result look like and what residual
   legacy auth sources are commonly missed?
3. Identity Secure Score dropped from {old_score} to {new_score}.
   How do you investigate the cause? Where do you see the score history
   and individual action status changes?
4. Extend log retention to {retention_requirement} months to meet the
   audit requirement. What are the two methods to achieve this and
   what is the cost difference? What Microsoft commitment covers
   log integrity and tamper-proofing?
5. Configure automated response to risky sign-ins using:
   a) Conditional Access risk-based policy (preventive)
   b) Microsoft Sentinel playbook (reactive)
   What is the difference between the two approaches and when would you
   use each?
""",
        "variables": {
            "org_name": ["Contoso Health", "Northwind Bank", "Pacific Insurance", "Alpine Council"],
            "score_period": ["3", "6", "12"],
            "retention_requirement": ["12", "24", "36"],
            "old_score": ["72", "68", "81", "59"],
            "new_score": ["54", "48", "61", "38"],
            "current_retention": ["7", "30"],
        },
        "exam_objectives": ["4.4"],
        "difficulty": "advanced",
        "answers": """
ANSWER GUIDE -- SC4-004-C: Identity Monitoring for Audit Compliance
 
Q1 -- Three privileged access alerts
 
Alert 1 -- Break-glass account usage:
AuditLogs
| where InitiatedBy.user.userPrincipalName in ("breakglass1@org.onmicrosoft.com",
    "breakglass2@org.onmicrosoft.com")
Severity: Critical. Action: immediate page to security team and CIO.
 
Alert 2 -- PIM activation outside business hours:
AuditLogs
| where OperationName == "Add member to role"
| where hourofday(TimeGenerated) !between (7 .. 19)
    or dayofweek(TimeGenerated) in (0d, 6d) // weekend
Severity: High.
 
Alert 3 -- Role assigned to guest user:
AuditLogs
| where OperationName == "Add member to role"
| where TargetResources[0].userPrincipalName contains "#EXT#"
Severity: High. Guest users should rarely receive directory roles.
 
Q2 -- Proving legacy auth elimination
Workbook: "Sign-ins using legacy authentication"
Path: Entra admin centre > Monitoring > Workbooks.
Clean result: zero rows in the "Sign-in count" column for all legacy protocols.
Commonly missed legacy auth sources:
  - SMTP AUTH (used by printers, scanners, legacy apps sending email)
  - POP3/IMAP (older email clients, mobile apps with old configurations)
  - Exchange Web Services (EWS) used by older Outlook versions
  - PowerShell with basic auth (older automation scripts)
These appear in the workbook even after modern auth is enforced -- they
represent sources that were blocked but still attempting connections.
 
Q3 -- Investigating Secure Score drop
Path: Entra admin centre > Security > Identity Secure Score.
History tab: shows score over time with trend chart.
Improvement actions tab: shows each action and its current status.
Filter by "Status = Regressed" to see which actions changed from
completed to incomplete (e.g. a CA policy was deleted, SSPR was disabled).
Common causes of score drop: policy deletion, licence expiry removing
a feature, new users added who are not covered by existing policies.
 
Q4 -- Extending log retention
Method 1 -- Log Analytics Workspace retention settings:
  Log Analytics > Usage and estimated costs > Data retention.
  Configurable up to 2 years (730 days). Higher retention = higher cost.
  Cost: approximately $0.10-0.12 per GB per month for retention beyond 90 days.
Method 2 -- Archive to Azure Storage Account:
  Diagnostic Settings > Storage Account destination.
  Cost: significantly cheaper (blob storage pricing ~$0.018/GB/month).
  Trade-off: not queryable directly -- must import back to Log Analytics for analysis.
Tamper-proofing: Azure Storage immutable blob storage (WORM policy) prevents
deletion or modification of logs for the compliance period.
Microsoft log integrity commitment: Entra logs are signed and tamper-evident
when stored in Log Analytics -- audit trails cannot be modified.
 
Q5 -- Preventive vs reactive response
 
a) Conditional Access risk-based policy (preventive):
  Entra > Security > CA > New policy > Conditions: Sign-in risk = High >
  Grant: Require MFA OR Block access.
  Fires BEFORE the sign-in completes -- user is challenged or blocked
  in real time. No human intervention required.
  Use when: you want automatic, immediate response at sign-in time.
 
b) Sentinel playbook (reactive):
  Sentinel > Automation > Playbook (Logic App).
  Triggers AFTER a risky event is logged -- response is seconds to minutes later.
  Actions: revoke user sessions (Graph API), notify security team,
  create incident ticket, disable account if risk is confirmed.
  Use when: the sign-in has already occurred and you need to contain the damage
  and initiate investigation. More flexible than CA (can do multi-step responses).
Both approaches are complementary -- CA prevents, Sentinel responds and investigates.
"""
    },
]
 
# ════════════════════════════════════════════════════════════════════════════
# UPDATED DOMAIN4_SCENARIOS list
# Replace the existing DOMAIN4_SCENARIOS in sc300_module.py with this
# ════════════════════════════════════════════════════════════════════════════
 
DOMAIN4_SCENARIOS = SC4_001_TEMPLATES + SC4_002_TEMPLATES + SC4_003_TEMPLATES + SC4_004_TEMPLATES
 

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
# ── Scenario ID search (sc300_search_patch) ──────────────────────────────────
from pbq.sc300_search_patch import (
    generate_sc300_pbq_by_id,
    display_sc300_pbq_with_nudge,
    show_sc300_scenario_index,
    SC300_SCENARIO_INDEX,
    SC300_SCENARIO_TOPICS,
)
