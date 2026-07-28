"""
GIDEON SC-300 Case Study Module
================================
Ten full-length, exam-style case studies (CS1-CS10) for Microsoft SC-300.
Each case study = 8 scored MCQ questions with full distractor analysis,
tagged by domain, plus a cross-referenced pattern library.

Structure mirrors sc300_module.py conventions:
  - generate_case_study_pbq() / get_weighted_case_study_pbq() / display_case_study_pbq()
  - domain_filter, difficulty_filter, case_study_filter
  - student_mode hides answers/explanations

CS10 (Meridian Group) is tagged difficulty="final_boss" -- it integrates all
four domains simultaneously and should be surfaced as its own tier once a
student has cleared CS1-CS9.
"""

import random
import re

CASE_STUDY_EXAM = {
    "code": "SC-300-CS",
    "name": "SC-300 Case Study Library",
    "version": "2026-07",
    "domains": {
        "1": {"name": "Implement and Manage User Identities", "weight": "20-25"},
        "2": {"name": "Implement Authentication and Access Management", "weight": "25-30"},
        "3": {"name": "Plan and Implement Workload Identities", "weight": "20-25"},
        "4": {"name": "Plan and Automate Identity Governance", "weight": "25-30"},
    },
}

# --------------------------------------------------------------------------
# CASE STUDY METADATA -- one entry per case study, condensed context so each
# question is self-contained without repeating the full 5-page scenario.
# --------------------------------------------------------------------------

CASE_STUDY_META = {
    "CS1": {
        "title": "Fabrikam Healthcare",
        "focus": "Core identity governance, PIM, CA baseline, shared workstations, hybrid SSPR",
        "context": (
            "Fabrikam Healthcare -- Wellington NZ hospital network, hybrid Entra ID (P2 staff / "
            "P1 contractors). 280 shared ward workstations, 14 permanent Global Admins, no PIM, "
            "SMS-only MFA, 340 legacy auth sign-ins/day, Southern Cross merger added 180 partner "
            "users as internal members (needs fixing), helpdesk has tenant-wide User Admin."
        ),
        "domains": ["1", "2", "4"],
    },
    "CS2": {
        "title": "Contoso Financial Services",
        "focus": "ID Protection risk policies, PIM hours/justification, insider risk, stale contractors",
        "context": (
            "Contoso Financial -- Auckland/Sydney/Singapore investment bank, hybrid with PHS enabled, "
            "ID Protection on but no risk policies, 6 permanent Global Admins, Purview E5 licensed but "
            "Insider Risk not configured, 34 stale contractor accounts, one trusted named location "
            "(Auckland only)."
        ),
        "domains": ["1", "2", "4"],
    },
    "CS3": {
        "title": "Alpine University",
        "focus": "B2B invitation vs cross-tenant sync vs entitlement management vs External ID",
        "context": (
            "Alpine University -- cloud-only, P2 staff / Free students, 1,240 unreviewed B2B guests, "
            "no Entitlement Management, no Access Reviews. External partners: 3 government research "
            "agencies (permanent), 12 corporate sponsors (project-based), 40 visiting institutions "
            "(short-term), 2,400 student interns, 15,000 online students needing consumer sign-in."
        ),
        "domains": ["1", "4"],
    },
    "CS4": {
        "title": "Pacific Government Agency",
        "focus": "Global Secure Access architecture, phishing-resistant MFA, CBA, Compliant Network CA",
        "context": (
            "Pacific Government Agency -- Entra Suite licensed, hybrid with PHS, Cisco AnyConnect VPN "
            "causing lateral-movement incidents, GSA not yet configured, 240 field staff on shared "
            "devices needing certificate auth, 8 regional offices, M365 traffic hairpinned through VPN."
        ),
        "domains": ["2"],
    },
    "CS5": {
        "title": "Northwind Retail Group",
        "focus": "Dynamic groups, group-based licensing, SSPR at scale, Lifecycle Workflows, privilege creep",
        "context": (
            "Northwind Retail -- 28,000 staff, cloud-only, 35% annual turnover, 847 stale assigned "
            "groups, no SSPR, no Lifecycle Workflows, Workday HR not yet SCIM-integrated, 3,400 stale "
            "former-employee accounts, 890 accounts with privilege creep, EuroStyle acquisition (4,500 "
            "users) pending migration."
        ),
        "domains": ["1"],
    },
    "CS6": {
        "title": "Southland Manufacturing",
        "focus": "Hybrid identity migration, PHS vs PTA vs AD FS, Seamless SSO, Staged Rollout, sequencing",
        "context": (
            "Southland Manufacturing -- 12,000 staff, on-prem AD since 1998, AD FS 2016 farm (3 outages "
            "in 18 months) federating all M365 auth, PHS configured but disabled, 12 legacy apps on "
            "AD FS, CTO mandate to eliminate on-prem auth dependency within 12 months."
        ),
        "domains": ["1", "2"],
    },
    "CS7": {
        "title": "TailwindTraders",
        "focus": "Managed Identities, delegated vs application permissions, SCIM, App Proxy, workload identity risk",
        "context": (
            "TailwindTraders -- 6,200 staff, cloud-only, P2 + Workload Identities Premium, 234 app "
            "registrations, 67 apps with hardcoded credentials, 12 shared service account passwords, "
            "34 apps with excessive API permissions, Salesforce provisioned manually, one legacy "
            "on-prem IIS app (LegacyWarehouse) needing remote access without modification."
        ),
        "domains": ["3"],
    },
    "CS8": {
        "title": "BlueSky Media Group",
        "focus": "Copilot governance, sensitivity labels, shadow AI, Verified ID, Copilot audit",
        "context": (
            "BlueSky Media -- 4,800 staff, cloud-only, M365 E5 + Copilot for all staff (including 180 "
            "contractor B2B guests), no Copilot governance, no sensitivity labels, 340 staff using "
            "personal ChatGPT (shadow AI), freelance talent need contract sign-in without Microsoft "
            "accounts."
        ),
        "domains": ["2", "4"],
    },
    "CS9": {
        "title": "Woodgrove Health Network",
        "focus": "Access Reviews at scale, Entitlement Management, GSA Internet Access, KQL, Secure Score",
        "context": (
            "Woodgrove Health -- 8,400 staff + 1,200 contractors, P2 staff / P1 contractors, no Access "
            "Reviews run in 18 months, 2,800 accounts needing review, 340 external partner users on "
            "direct group membership, Secure Score dropped 74->61, no web content filtering on clinical "
            "devices, no KQL alerting configured."
        ),
        "domains": ["2", "4"],
    },
    "CS10": {
        "title": "Meridian Group (The Final Boss)",
        "focus": "ALL DOMAINS INTEGRATED -- GSA, Copilot, PIM, hybrid, lifecycle, ID Protection, entitlement, workload identity",
        "context": (
            "Meridian Group -- 18,000 staff + 4,000 contractors, 34 countries, hybrid (3 forests, PHS), "
            "TechVentures acquisition (2,800 staff) pending integration, three board-level incidents: "
            "6-month-stale leaver account used for exfiltration, Copilot summarised a privileged legal "
            "document via stale group access, 23 Azure apps with hardcoded credentials found on GitHub. "
            "90-day CISO mandate covering all four SC-300 domains simultaneously."
        ),
        "domains": ["1", "2", "3", "4"],
    },
}

# --------------------------------------------------------------------------
# QUESTIONS -- 8 per case study, 80 total.
# domain: "1"-"4", or combined e.g. "2+4" for cross-domain (CS10 only)
# --------------------------------------------------------------------------

CASE_STUDY_QUESTIONS = [

    # ============================== CS1 -- Fabrikam Healthcare ==============
    {"id": "CS1-Q1", "case_study": "CS1", "domain": "2", "difficulty": "intermediate",
     "question": "Which authentication method satisfies BR1 -- clinical staff authenticate to shared ward workstations WITHOUT a smartphone?",
     "options": {"A": "Microsoft Authenticator push notification", "B": "SMS one-time passcode",
                 "C": "FIDO2 security key", "D": "Windows Hello for Business"},
     "correct": "C",
     "explanation": ("FIDO2 security key. BR1 explicitly rules out smartphone-based methods (A, B). WHfB (D) needs "
                      "per-user device enrollment on a dedicated device -- fails on shared ward PCs. FIDO2 is a "
                      "hardware token any user can tap on any shared workstation, and it's phishing-resistant."),
     "pattern_refs": ["Phishing-resistant MFA = FIDO2/WHfB/CBA only"]},

    {"id": "CS1-Q2", "case_study": "CS1", "domain": "4", "difficulty": "intermediate",
     "question": "What is the minimum number of Global Administrator accounts Fabrikam should retain as PERMANENT after implementing SR2 (max 4 GAs, no permanent standing access)?",
     "options": {"A": "1", "B": "2", "C": "4", "D": "14"},
     "correct": "B",
     "explanation": ("2 permanent break-glass accounts. Microsoft best practice is exactly 2 -- a single break-glass "
                      "account is a single point of failure; the remaining GAs (up to 4 total per SR2) move to PIM "
                      "eligible, not permanent."),
     "pattern_refs": ["PIM: break-glass = exactly 2, permanent, excluded from all CA"]},

    {"id": "CS1-Q3", "case_study": "CS1", "domain": "2", "difficulty": "intermediate",
     "question": "Which action must be completed BEFORE enabling the Block Legacy Authentication CA policy, given 340 legacy auth sign-ins/day are still detected?",
     "options": {"A": "Enable Password Hash Sync on Entra Connect", "B": "Convert the legacy auth policy from Report-only to On immediately",
                 "C": "Review the legacy authentication workbook and remediate remaining legacy auth sources", "D": "Disable AD FS before blocking legacy auth"},
     "correct": "C",
     "explanation": ("Review the sign-ins-using-legacy-auth workbook, identify sources (printers, scanners, old "
                      "scripts), remediate them, then flip Policy 2 to On. Blocking immediately would break active "
                      "services. TR5 requires report-only testing before enforcement."),
     "pattern_refs": ["Always check the legacy-auth workbook before blocking"]},

    {"id": "CS1-Q4", "case_study": "CS1", "domain": "4", "difficulty": "advanced",
     "question": "Which solution satisfies BR5 -- helpdesk can only reset passwords for their OWN department?",
     "options": {"A": "Assign Password Administrator to all helpdesk staff (tenant scope)",
                 "B": "Assign Authentication Administrator scoped to an Administrative Unit per department",
                 "C": "Assign Authentication Administrator at tenant scope", "D": "Create a custom role with password-reset permissions at tenant scope"},
     "correct": "B",
     "explanation": ("Authentication Administrator scoped to an AU per department. AUs restrict the role to only "
                      "the users in that AU -- a Finance helpdesk agent can't touch Clinical or IT users. Any "
                      "tenant-scoped role (A, C, D) fails BR5 regardless of which role is chosen."),
     "pattern_refs": ["Scope (Administrative Units) solves department-restriction requirements"]},

    {"id": "CS1-Q5", "case_study": "CS1", "domain": "4", "difficulty": "intermediate",
     "question": "Which PIM setting satisfies SR5 -- privileged role activations require justification AND are time-limited to 4 hours MAXIMUM (plus SR1 phishing-resistant MFA for admin actions)?",
     "options": {"A": "Require MFA, maximum 8 hours, no approval required", "B": "Require justification, maximum 4 hours, require MFA",
                 "C": "Require approval, maximum 24 hours, justification optional", "D": "No MFA required, maximum 4 hours, require justification"},
     "correct": "B",
     "explanation": ("Justification + 4hr max + MFA satisfies SR5 (justification, 4hr max) and SR1 (MFA for admin "
                      "actions) simultaneously. A exceeds the hour limit. C exceeds the limit and makes justification "
                      "optional. D drops MFA, violating SR1."),
     "pattern_refs": ["PIM: max activation 4-8hrs, always require MFA + justification for privileged roles"]},

    {"id": "CS1-Q6", "case_study": "CS1", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies BR2 -- password reset without helpdesk involvement -- in this HYBRID environment?",
     "options": {"A": "Enable SSPR for All users including contractors", "B": "Enable SSPR for Clinical-Staff-All and IT-Administrators groups only",
                 "C": "Enable SSPR for All users AND configure password writeback", "D": "Enable SSPR for a selected group of staff only"},
     "correct": "C",
     "explanation": ("SSPR + writeback. Without writeback, a cloud SSPR reset never reaches on-prem AD -- users stay "
                      "locked out of domain-joined systems and still need the helpdesk. Writeback is the mandatory "
                      "companion to SSPR in any hybrid scenario."),
     "pattern_refs": ["Writeback before/with SSPR in hybrid environments"]},

    {"id": "CS1-Q7", "case_study": "CS1", "domain": "1", "difficulty": "advanced",
     "question": "Which solution satisfies SR7 -- Southern Cross partner users must complete MFA even if their home tenant already enforces MFA?",
     "options": {"A": "Configure Cross-Tenant Access Settings to trust MFA from the Southern Cross tenant",
                 "B": "Create a CA policy targeting guest users requiring MFA, without trusting cross-tenant MFA claims",
                 "C": "Migrate Southern Cross users from B2B guests to internal member accounts", "D": "Enable Security Defaults"},
     "correct": "B",
     "explanation": ("CA policy on guest users requiring MFA with cross-tenant trust NOT enabled. 'Regardless of "
                      "home tenant' always means don't trust -- trusting (A) is the literal opposite of the "
                      "requirement. C breaks BR3 (partners governed separately). D can't coexist with existing CA."),
     "pattern_refs": ["MFA regardless of home tenant = CA policy with no cross-tenant MFA trust"]},

    {"id": "CS1-Q8", "case_study": "CS1", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies TR1 -- Clinical-Staff-All group membership updates AUTOMATICALLY when HR attributes change?",
     "options": {"A": "Dynamic group rule: (user.jobTitle -eq 'Nurse') or (user.jobTitle -eq 'Doctor') or (user.jobTitle -eq 'Pharmacist')",
                 "B": "Dynamic group rule: (user.department -eq 'Clinical')",
                 "C": "Keep as an assigned group with a weekly PowerShell update script", "D": "A Lifecycle Workflow that adds users on employeeHireDate"},
     "correct": "B",
     "explanation": ("Dynamic group on department. jobTitle (A) is fragile -- every new title needs a rule update. "
                      "A weekly script (C) isn't attribute-triggered and lags up to 7 days. A Lifecycle Workflow (D) "
                      "handles onboarding but not the mover scenario when someone changes departments."),
     "pattern_refs": ["Department over jobTitle for dynamic groups -- stable attribute, broad coverage"]},

    # ============================== CS2 -- Contoso Financial Services ========
    {"id": "CS2-Q1", "case_study": "CS2", "domain": "2", "difficulty": "intermediate",
     "question": "Which CA policy configuration satisfies SR1 -- automatically block HIGH risk sign-ins (modern CA approach, not the legacy ID Protection portal)?",
     "options": {"A": "In ID Protection, configure the Sign-in risk policy to block High risk sign-ins",
                 "B": "CA policy: Conditions > Sign-in risk = High > Grant = Block access",
                 "C": "Sentinel alert notifying the security team of High risk sign-ins", "D": "Extend the existing Require MFA policy to also apply to High risk sign-ins"},
     "correct": "B",
     "explanation": ("Modern CA policy with Sign-in risk = High > Block. TR1 explicitly rules out the legacy ID "
                      "Protection portal (A). An alert (C) requires human response -- SR1 wants automatic block. "
                      "MFA step-up (D) doesn't stop an attacker who already has the MFA device, as incident 1 showed."),
     "pattern_refs": ["Legacy ID Protection portal = wrong when TR says modern CA approach"]},

    {"id": "CS2-Q2", "case_study": "CS2", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies BR2 -- Sydney and Singapore get no MFA prompt on corporate networks, without adding friction for existing Auckland users (TR4)?",
     "options": {"A": "Create separate CA policies for Sydney and Singapore that skip MFA",
                 "B": "Add Sydney and Singapore IP ranges to Policy 3's existing trusted named locations",
                 "C": "Disable the Require MFA policy for Sydney/Singapore users", "D": "Create new named locations and new CA policies excluding those locations"},
     "correct": "B",
     "explanation": ("Extend the existing Policy 3 (which already trusts Auckland) rather than building new "
                      "policies. This satisfies TR4 (no change to Auckland behaviour) and the minimum-policies "
                      "principle. C removes MFA entirely, even off-network -- a security regression."),
     "pattern_refs": ["Extend existing CA policy rather than duplicating when scope allows"]},

    {"id": "CS2-Q3", "case_study": "CS2", "domain": "4", "difficulty": "advanced",
     "question": "Which solution satisfies SR5 -- insider risk signals feed into CA -- given TR2 (existing licences only, and Purview E5 is already available but unconfigured)?",
     "options": {"A": "Purchase Microsoft Entra ID Governance for insider risk CA integration",
                 "B": "Configure the Insider Risk CA condition using Microsoft Purview Insider Risk Management signals",
                 "C": "Sentinel KQL queries that trigger CA policy changes", "D": "Enable Microsoft Defender for Cloud Apps anomaly detection"},
     "correct": "B",
     "explanation": ("Purview Insider Risk Management is already licensed (E5) -- just needs configuring. The CA "
                      "Insider Risk condition consumes its signal directly. A violates TR2 (no new licences needed "
                      "when one's already available). C isn't how CA works -- policies are static, not dynamically rewritten."),
     "pattern_refs": ["Check existing licences before assuming a purchase is needed"]},

    {"id": "CS2-Q4", "case_study": "CS2", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies BR1 and TR3 -- automatically disable stale contractor accounts after 90 days inactivity, with no manual admin intervention after setup?",
     "options": {"A": "Access Review targeting contractors, auto-apply, 90-day recurrence", "B": "Lifecycle Workflow with an attribute-based trigger on lastSignInDateTime",
                 "C": "Monthly PowerShell script disabling accounts inactive 90+ days", "D": "Set a fixed 90-day account expiry date at creation"},
     "correct": "B",
     "explanation": ("Lifecycle Workflow on lastSignInDateTime fires automatically with zero manual intervention. "
                      "Access Reviews (A) still need a human reviewer to respond even with auto-apply. A script (C) "
                      "requires scheduling/execution. Fixed expiry (D) ignores actual activity."),
     "pattern_refs": ["Lifecycle Workflow for automatic inactivity disable -- Access Review needs a human"]},

    {"id": "CS2-Q5", "case_study": "CS2", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies SR2 -- HIGH risk USER accounts are automatically forced to reset their password (not blocked outright)?",
     "options": {"A": "ID Protection User risk policy requiring password change for High risk (legacy portal)",
                 "B": "CA policy: Conditions > User risk = High > Grant = Require password change",
                 "C": "CA policy: Conditions > User risk = High > Grant = Block access", "D": "Sentinel playbook resetting passwords when High risk is detected"},
     "correct": "B",
     "explanation": ("Modern CA with Require password change lets the user self-remediate via SSPR. TR1 rules out "
                      "the legacy portal (A). Block (C) is a permanent lockout with no recovery path -- SR2 wants "
                      "reset, not lockout. Sentinel (D) is reactive and slower than CA firing at sign-in."),
     "pattern_refs": ["Require password change != Block -- reset gives a recovery path"]},

    {"id": "CS2-Q6", "case_study": "CS2", "domain": "2", "difficulty": "advanced",
     "question": "Which solution satisfies BR4 -- financial analysts blocked outside 8am-6pm NZST UNLESS on an approved exception list?",
     "options": {"A": "CA policy on Financial-Analysts with a time condition and Grant = Block (no exception)",
                 "B": "A named location called 'Business Hours' excluding analysts outside it",
                 "C": "CA policy with a sign-in frequency condition", "D": "CA policy on Financial-Analysts with a time condition, Grant = Block, plus an excluded exception group"},
     "correct": "D",
     "explanation": ("The exception clause is the detail that separates A from D -- BR4 explicitly requires an "
                      "approved exception list, implemented as an excluded group in the CA policy. Named locations "
                      "(B) are IP/country-based, not time-based. Sign-in frequency (C) controls re-prompt cadence, not blocking."),
     "pattern_refs": ["Read every clause of a requirement -- an exception clause changes the correct answer"]},

    {"id": "CS2-Q7", "case_study": "CS2", "domain": "1", "difficulty": "intermediate",
     "question": "What is the FIRST action to remediate the 34 stale contractor accounts identified in SR4 (immediate remediation required)?",
     "options": {"A": "Delete all 34 accounts immediately", "B": "Disable all 34 accounts and revoke their active sessions",
                 "C": "Run an Access Review and wait for reviewer decisions", "D": "Reset passwords on all 34 accounts"},
     "correct": "B",
     "explanation": ("Disable + revoke sessions today. Never hard-delete immediately (audit trail, 30-day "
                      "retention). Access Review (C) is too slow for an 'immediately' requirement. Password reset "
                      "(D) doesn't help if an attacker already holds a session token."),
     "pattern_refs": ["Disable before delete -- never immediate deletion"]},

    {"id": "CS2-Q8", "case_study": "CS2", "domain": "4", "difficulty": "intermediate",
     "question": "Which configuration satisfies SR6 -- Global Admin activations logged with justification, limited to 2 hours MAXIMUM?",
     "options": {"A": "PIM: maximum activation 2 hours, require MFA, require justification",
                 "B": "CA policy requiring MFA for Global Admin with a 2-hour session timeout",
                 "C": "PIM: maximum activation 4 hours, require approval, require justification", "D": "Sentinel alert firing on Global Admin activation"},
     "correct": "A",
     "explanation": ("PIM role settings directly control max duration, MFA, and justification. C's 4-hour max "
                      "violates SR6's explicit 2-hour cap. CA session timeout (B) isn't the same as PIM activation "
                      "duration. Sentinel (D) is after-the-fact, not enforcement at activation."),
     "pattern_refs": ["PIM: max activation hours must match the exact SR figure -- read the number"]},

    # ============================== CS3 -- Alpine University =================
    {"id": "CS3-Q1", "case_study": "CS3", "domain": "1", "difficulty": "advanced",
     "question": "Which solution satisfies BR2 and TR1 for the 45 government agency researchers -- seamless internal-looking appearance, no individual invitations?",
     "options": {"A": "Send B2B invitations to all 45 researchers individually", "B": "Configure Cross-Tenant Synchronization with the government agency tenants",
                 "C": "Connected Organization + access packages for the researchers", "D": "Add the 45 researchers as internal member accounts"},
     "correct": "B",
     "explanation": ("Cross-tenant sync is a push model that provisions B2B members (not guests) -- appearing "
                      "internal in Teams/directory. TR1 rules out individual invitations (A). C is the right tool for "
                      "project-scoped sponsors, not permanent strategic partners. D creates unnecessary licence cost."),
     "pattern_refs": ["Cross-tenant sync = internal/acquisition appearance. B2B = guest. External ID = consumers"]},

    {"id": "CS3-Q2", "case_study": "CS3", "domain": "4", "difficulty": "advanced",
     "question": "Which solution satisfies BR1, BR3, and TR2 for corporate research sponsors -- self-service request, auto-removal at project end, access packages not direct groups?",
     "options": {"A": "B2B invitations + direct security group assignment", "B": "Connected Organizations + access packages per sponsor project with automatic expiry",
                 "C": "Cross-Tenant Sync to provision sponsors as B2B members", "D": "A single access package for all sponsors with a 24-month expiry"},
     "correct": "B",
     "explanation": ("Access packages give self-service requests (BR1) and automatic expiry at project end (BR3). "
                      "TR2 rules out direct group assignment (A). Cross-tenant sync (C) suits permanent partners, "
                      "not project-based ones. A single shared package (D) can't scope different resources per sponsor."),
     "pattern_refs": ["Entitlement Management: catalog -> resources -> access package -> policy"]},

    {"id": "CS3-Q3", "case_study": "CS3", "domain": "2", "difficulty": "advanced",
     "question": "Which solution satisfies SR4 -- DataVault access requires MFA regardless of home tenant MFA status?",
     "options": {"A": "Cross-Tenant Access Settings trusting MFA from all partner tenants", "B": "Security Defaults requiring MFA for all users including guests",
                 "C": "CA policy targeting DataVault requiring MFA, without trusting cross-tenant MFA claims", "D": "Require MFA as part of the DataVault access package policy"},
     "correct": "C",
     "explanation": ("CA policy with no cross-tenant MFA trust enabled. A is the literal opposite of the "
                      "requirement. Security Defaults (B) can't coexist with existing CA policies. Access packages "
                      "(D) can't enforce MFA -- that's a CA function only."),
     "pattern_refs": ["MFA regardless of home tenant = CA policy no cross-tenant trust"]},

    {"id": "CS3-Q4", "case_study": "CS3", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies SR1 and TR6 -- review all 1,240 guest accounts and auto-remove where a reviewer doesn't respond?",
     "options": {"A": "Single Access Review: all guest users, quarterly, auto-apply, reviewer = sponsor, no response = Remove access",
                 "B": "Access Reviews per partner type with manual result application", "C": "PowerShell script disabling guests with no sign-in in 90 days",
                 "D": "Guest account expiry set to 12 months for all guests"},
     "correct": "A",
     "explanation": ("One review scoped to all guests, auto-apply ON, no-response = Remove. B fails TR6 since "
                      "manual application means denials never actually take effect. C only catches sign-in "
                      "inactivity, not a genuine reviewer decision. D gives no renewal decision point, just a blunt cutoff."),
     "pattern_refs": ["Access Reviews: auto-apply + no response = remove + fallback reviewers"]},

    {"id": "CS3-Q5", "case_study": "CS3", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies BR6 and TR4 -- 15,000 online students sign in with their existing Google or Microsoft personal accounts?",
     "options": {"A": "Internal member accounts for all 15,000 students", "B": "Google federation in External Identities + B2B guest invitations",
                 "C": "Microsoft Entra External ID with Google and Microsoft account identity providers", "D": "Security Defaults allowing personal Microsoft accounts"},
     "correct": "C",
     "explanation": ("External ID (consumer identity) is purpose-built for exactly this scale and scenario. TR4 "
                      "rules out internal member accounts (A). B2B (B) is for business partners, not consumers, and "
                      "15,000 individual invitations is unmanageable. Security Defaults (D) doesn't configure identity providers."),
     "pattern_refs": ["Cross-tenant sync = internal/acquisition. B2B = partners. External ID = consumers"]},

    {"id": "CS3-Q6", "case_study": "CS3", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies BR5 and TR5 -- visiting academics accept a Terms of Use before accessing research systems, enforced via CA not manual process?",
     "options": {"A": "ToU checkbox on the access package request form", "B": "Terms of Use policy (PDF) enforced via a CA policy targeting research applications",
                 "C": "Email the ToU document and require email acknowledgement", "D": "Configure ToU in Connected Organization settings"},
     "correct": "B",
     "explanation": ("ToU lives in Identity Governance and is enforced via CA -- access packages (A) and Connected "
                      "Organizations (D) have no ToU functionality. Email (C) is explicitly the manual process TR5 rules out."),
     "pattern_refs": ["ToU = CA enforcement not manual -- PDF format required"]},

    {"id": "CS3-Q7", "case_study": "CS3", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies SR2 -- guests cannot enumerate the full directory or see other guest accounts?",
     "options": {"A": "Assign Security Reader role to all guest accounts", "B": "External Collaboration settings: Guest user access = Most restrictive",
                 "C": "CA policy blocking guest access to the Entra admin centre", "D": "Remove all guest accounts from security groups"},
     "correct": "B",
     "explanation": ("Directory enumeration is governed by the tenant-wide External Collaboration setting, not a "
                      "CA policy. A actually increases guest permissions -- the opposite of what's needed. C and D "
                      "don't touch the underlying directory-visibility setting."),
     "pattern_refs": ["Directory enumeration is a settings page, not a CA policy"]},

    {"id": "CS3-Q8", "case_study": "CS3", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies BR4 -- student intern guest accounts automatically disabled when placement ends (each intern has a different 3-6 month end date)?",
     "options": {"A": "6-month global expiry on all guest accounts", "B": "Quarterly Access Review targeting intern guests",
                 "C": "Access package for intern access with expiry matching the placement end date, Renewal = No", "D": "Lifecycle Workflow triggered by placement end date"},
     "correct": "C",
     "explanation": ("Access packages support per-assignment expiry matching each individual's actual placement "
                      "end date, with Renewal = No preventing accidental extension. A global expiry (A) can't match "
                      "individual dates. Lifecycle Workflows (D) govern internal users, not B2B guests."),
     "pattern_refs": ["Lifecycle Workflows = internal users. Guest lifecycle = access packages"]},

    # ============================== CS4 -- Pacific Government Agency =========
    {"id": "CS4-Q1", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which GSA component satisfies BR1 -- Zero Trust remote access to internal apps, replacing the VPN?",
     "options": {"A": "GSA Internet Access with web filtering for internal app URLs", "B": "GSA Private Access with application segments per internal app",
                 "C": "GSA Microsoft 365 traffic profile", "D": "Azure Application Proxy"},
     "correct": "B",
     "explanation": ("Private Access with app segments gives app-by-app ZTNA -- no lateral movement, unlike the "
                      "flat VPN. Internet Access (A) filters outbound web traffic, not internal apps. The M365 "
                      "profile (C) is unrelated. App Proxy (D) is the older HTTP-only predecessor to GSA."),
     "pattern_refs": ["GSA Private Access = replaces VPN, app-by-app ZTNA"]},

    {"id": "CS4-Q2", "case_study": "CS4", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies BR2 and TR3 -- M365 traffic must not be hairpinned through the VPN, using the built-in GSA profile?",
     "options": {"A": "VPN split tunnelling excluding M365 IP ranges", "B": "Enable the GSA Microsoft 365 traffic forwarding profile for all users",
                 "C": "CA named location excluding M365 from VPN policy", "D": "DNS routing M365 traffic around the VPN"},
     "correct": "B",
     "explanation": ("TR3 specifically requires the built-in GSA M365 profile, not a custom VPN or DNS "
                      "workaround. Named locations (C) control CA policy application, not traffic routing."),
     "pattern_refs": ["M365 Traffic Profile = built-in GSA feature, no custom config needed"]},

    {"id": "CS4-Q3", "case_study": "CS4", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies SR3 -- the Private Network Connector requires NO inbound firewall rules?",
     "options": {"A": "Install in the DMZ, open inbound port 443", "B": "Install on an internal network server -- outbound HTTPS only",
                 "C": "Install on a public-facing server with a public IP", "D": "Use a site-to-site VPN tunnel for connectivity"},
     "correct": "B",
     "explanation": ("The connector always initiates outbound HTTPS to the GSA edge -- it never receives inbound "
                      "connections, so it belongs on any internal server behind the firewall. A, C, and D all "
                      "introduce unnecessary inbound exposure that the architecture doesn't require."),
     "pattern_refs": ["GSA connector = outbound HTTPS only, no inbound rules, internal server"]},

    {"id": "CS4-Q4", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which solution satisfies BR4 -- 8 regional branch offices access GSA without installing a client on every device?",
     "options": {"A": "Deploy the GSA client via Intune to all branch devices", "B": "Remote Network Connectivity using an IPsec/BGP tunnel from branch routers",
                 "C": "Install the Private Network Connector at each branch", "D": "CA named locations for branch IP ranges"},
     "correct": "B",
     "explanation": ("Remote Network Connectivity tunnels the entire branch network through GSA at the router "
                      "level -- no per-device client needed, which TR2 explicitly requires. The Connector (C) "
                      "publishes on-prem apps, it doesn't route branch traffic."),
     "pattern_refs": ["Remote Network Connectivity = branch offices without per-device client"]},

    {"id": "CS4-Q5", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which solution satisfies SR5 AND SR1 -- prevent MFA fatigue AND require genuinely phishing-resistant MFA (the trap: number matching alone satisfies only one of these)?",
     "options": {"A": "Number matching on Authenticator, continue using push", "B": "Replace Authenticator with SMS OTP",
                 "C": "Deploy FIDO2 security keys to all staff", "D": "Number matching -- claims to satisfy both SR1 and SR5"},
     "correct": "C",
     "explanation": ("FIDO2 is the only option satisfying both: phishing-resistant (SR1) and immune to fatigue "
                      "attacks since there's no push to approve. Number matching (A, D) stops fatigue but "
                      "Authenticator push is still not phishing-resistant, no matter how the option is worded."),
     "pattern_refs": ["Number matching != phishing-resistant. FIDO2/WHfB/CBA = phishing-resistant"]},

    {"id": "CS4-Q6", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which solution satisfies SR6 and BR3 -- FieldApp uses CBA configured as MULTI-FACTOR on shared devices, no smartphone required?",
     "options": {"A": "Single-factor CBA for FieldApp", "B": "Multi-factor CBA -- map the certificate policy OID to MFA in Entra CBA settings",
                 "C": "WHfB on shared field devices with PIN", "D": "CA policy requiring MFA + existing Authenticator app"},
     "correct": "B",
     "explanation": ("OID-mapped multi-factor CBA makes the certificate itself satisfy MFA -- no second prompt "
                      "needed. Single-factor CBA (A) still requires a separate MFA step. WHfB (C) needs per-user "
                      "device enrollment, incompatible with shared devices. D requires a smartphone, violating BR3."),
     "pattern_refs": ["Single-factor vs multi-factor CBA -- OID mapping makes CBA count as MFA"]},

    {"id": "CS4-Q7", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which CA policy satisfies SR4 -- accessing internal apps WITHOUT going through GSA must be blocked?",
     "options": {"A": "Named location NOT corporate > Block", "B": "Compliant Network = No > Block",
                 "C": "Device compliance = No > Block", "D": "Restrict the Private Network Connector to GSA edge IPs only"},
     "correct": "B",
     "explanation": ("The Compliant Network CA condition is purpose-built to detect whether a sign-in came "
                      "through GSA. Named locations (A) block legitimate remote workers on non-corporate IPs. "
                      "Device compliance (C) doesn't detect GSA bypass -- a compliant device can still skip GSA."),
     "pattern_refs": ["Compliant Network CA condition = enforces GSA usage. Named locations do NOT"]},

    {"id": "CS4-Q8", "case_study": "CS4", "domain": "2", "difficulty": "advanced",
     "question": "Which CA policy satisfies SR2 -- CaseDB requires compliant device AND phishing-resistant MFA specifically?",
     "options": {"A": "Require MFA (either method)", "B": "Require compliant device AND Require MFA",
                 "C": "Require Authentication Strength (Phishing-resistant) AND Require compliant device", "D": "Block on High risk sign-in only"},
     "correct": "C",
     "explanation": ("Authentication Strength is the specific CA control that names which methods qualify -- 'Require "
                      "MFA' (A, B) accepts any method including SMS, which fails the phishing-resistant requirement. "
                      "D only blocks on risk, not as a baseline requirement."),
     "pattern_refs": ["Authentication Strength: phishing-resistant != Require MFA (any method)"]},

    # ============================== CS5 -- Northwind Retail Group ============
    {"id": "CS5-Q1", "case_study": "CS5", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies BR6 and TR1 -- automatic licence assignment that updates when HR attributes change?",
     "options": {"A": "Assign F3 licences directly to new store associate accounts", "B": "Dynamic security groups per staff category with group-based licensing",
                 "C": "Nightly PowerShell script assigning licences by department", "D": "Workday assigns licences directly via SCIM"},
     "correct": "B",
     "explanation": ("Dynamic groups update automatically on attribute change and drive licence assignment "
                      "without any manual step. A nightly script (C) introduces up to 24hrs delay. SCIM (D) "
                      "provisions/updates accounts -- it doesn't directly assign M365 licences, that's Entra's job."),
     "pattern_refs": ["Scale eliminates manual solutions -- dynamic groups over individual assignment"]},

    {"id": "CS5-Q2", "case_study": "CS5", "domain": "1", "difficulty": "advanced",
     "question": "Which solution satisfies SR2 and BR2 -- PREVENT privilege creep when staff change departments (not just detect it)?",
     "options": {"A": "Quarterly Access Reviews to find and remove old-department access", "B": "Mover Lifecycle Workflow that removes old group memberships BEFORE assigning new ones",
                 "C": "Require managers to submit an IT ticket on transfer", "D": "Dynamic groups only -- old membership removes automatically"},
     "correct": "B",
     "explanation": ("The remove-old-first sequencing in the Mover workflow is the key detail -- dynamic groups "
                      "(D) handle licence-linked groups but leave manually-assigned app access untouched, which is "
                      "exactly how the 890 privilege-creep accounts happened. Access Reviews (A) detect after the fact, not prevent."),
     "pattern_refs": ["Dynamic groups alone don't prevent privilege creep -- Lifecycle Workflow remove-first needed"]},

    {"id": "CS5-Q3", "case_study": "CS5", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies BR3 and SR3 -- seasonal workers lose access after exactly 13 weeks, no manual renewal without IT approval?",
     "options": {"A": "Lifecycle Workflow triggered 91 days after employeeHireDate", "B": "Account expiry dates set to 91 days at creation",
                 "C": "Access package for seasonal workers: 13-week expiry, Renewal allowed = No", "D": "Access Review for the seasonal group every 13 weeks"},
     "correct": "C",
     "explanation": ("Access packages with Renewal = No enforce a hard expiry that can't be overridden without a "
                      "brand-new IT-approved request. Account expiry (B) disables the whole account rather than "
                      "removing scoped resources. Access Review (D) can be overridden by a reviewer's approval."),
     "pattern_refs": ["Access packages for hard expiry, Lifecycle Workflows for process steps"]},

    {"id": "CS5-Q4", "case_study": "CS5", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies SR4 and TR3 -- Workday as the authoritative HR source, provisioning via SCIM not CSV?",
     "options": {"A": "Daily CSV export from Workday, bulk import to Entra", "B": "Workday SCIM 2.0 provisioning via the Entra provisioning service",
                 "C": "Entra Connect Cloud Sync from Workday", "D": "Workday HR connector in Microsoft Identity Manager"},
     "correct": "B",
     "explanation": ("Entra has a native Workday-to-Entra SCIM provisioning connector, satisfying TR3 directly. "
                      "CSV (A) is explicitly ruled out and introduces batch delay. Cloud Sync (C) syncs from "
                      "on-prem AD -- irrelevant here, this tenant is cloud-only. MIM (D) needs separate infrastructure/licensing."),
     "pattern_refs": ["SCIM provisioning over CSV -- always choose SCIM for HR system integration"]},

    {"id": "CS5-Q5", "case_study": "CS5", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies BR4 and SR5 -- SSPR for all 28,000 staff with 2-method registration enforced before helpdesk stops accepting resets?",
     "options": {"A": "Enable SSPR for a selected group, gradually expand", "B": "SSPR for All, registration campaign with 2 methods required, CA policy enforcing registration",
                 "C": "SSPR for All with only 1 method required", "D": "SSPR for All, wait for voluntary registration"},
     "correct": "B",
     "explanation": ("CA enforcement is what actually guarantees compliance before the helpdesk cutover -- "
                      "unregistered users are blocked from completing sign-in until they register. Voluntary "
                      "registration (D) won't reach the needed coverage at 28,000 users with 35% turnover."),
     "pattern_refs": ["SSPR CA enforcement: unregistered users cannot sign in until registered"]},

    {"id": "CS5-Q6", "case_study": "CS5", "domain": "1", "difficulty": "intermediate",
     "question": "What is the correct IMMEDIATE approach to identify and disable the 3,400 stale former-employee accounts (SR1)?",
     "options": {"A": "Delete all 3,400 accounts immediately", "B": "Access Review with auto-apply, wait 14 days",
                 "C": "PowerShell cross-referencing Workday termination status, disable immediately, verify in audit logs", "D": "Lifecycle Workflow applied retroactively to stale accounts"},
     "correct": "C",
     "explanation": ("SR1 says immediately -- Access Reviews (B) take too long. Lifecycle Workflows (D) only "
                      "process future events; they cannot retroactively fire on historical terminations. Never "
                      "delete immediately (A) -- disable and retain for audit trail."),
     "pattern_refs": ["Disable before delete -- never immediate deletion"]},

    {"id": "CS5-Q7", "case_study": "CS5", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies SR6 -- automatically identify and reclaim 1,200 stale licences from inactive seasonal accounts?",
     "options": {"A": "Monthly PowerShell script removing licences after 90 days no sign-in", "B": "Group-based licensing with dynamic groups -- inactive accounts fall out of scope automatically",
                 "C": "Access Review auto-removing licences for denied users", "D": "Manual quarterly licence report review"},
     "correct": "B",
     "explanation": ("Once Workday SCIM correctly reflects termination, the dynamic group condition (active + "
                      "seasonal) drops the account out of scope and the licence is reclaimed automatically -- fully "
                      "attribute-triggered, no manual step. A and D both lag behind actual terminations."),
     "pattern_refs": ["Group-based licensing auto-reclaims when the attribute condition changes"]},

    {"id": "CS5-Q8", "case_study": "CS5", "domain": "1", "difficulty": "advanced",
     "question": "Which solution satisfies BR5 and TR6 -- migrate 4,500 EuroStyle users into the Northwind tenant within 60 days, using cross-tenant migration tools?",
     "options": {"A": "Manually recreate all 4,500 accounts", "B": "Send B2B invitations to all 4,500 users",
                 "C": "Cross-Tenant Synchronization from the EuroStyle tenant to the Northwind tenant", "D": "CSV export/bulk PowerShell import"},
     "correct": "C",
     "explanation": ("This is an acquisition -- users become internal Northwind employees, so cross-tenant sync "
                      "(internal-looking members) is correct, not B2B guests (B, external appearance). TR6 rules "
                      "out manual recreation (A) and CSV (D), both of which lose mailbox/OneDrive content too."),
     "pattern_refs": ["Cross-tenant sync for acquisitions, B2B for partners"]},

    # ============================== CS6 -- Southland Manufacturing ===========
    {"id": "CS6-Q1", "case_study": "CS6", "domain": "1", "difficulty": "advanced",
     "question": "Which authentication method satisfies SR1, SR2, and TR5 -- enables ID Protection and cloud resilience (PTA explicitly ruled out)?",
     "options": {"A": "Continue AD FS, monitor more closely with Entra Connect Health", "B": "Switch to Pass-Through Authentication (PTA)",
                 "C": "Switch to Password Hash Synchronization (PHS)", "D": "Deploy a second AD FS farm for redundancy"},
     "correct": "C",
     "explanation": ("PHS enables ID Protection's leaked-credential detection (requires a hash in the cloud) and "
                      "keeps auth working even if on-prem is down -- directly addressing the three AD FS outages. "
                      "SR2 explicitly rules out PTA (B), which still depends on an on-prem agent."),
     "pattern_refs": ["PHS preferred over PTA -- enables ID Protection + cloud resilience"]},

    {"id": "CS6-Q2", "case_study": "CS6", "domain": "1", "difficulty": "advanced",
     "question": "Which approach satisfies TR1 and BR2 -- test cloud auth with a pilot group BEFORE domain conversion, with rollback capability?",
     "options": {"A": "Convert one of the three domains and test with that domain's users", "B": "Staged Rollout for cloud authentication with a pilot group",
                 "C": "Create a new test tenant and migrate 100 users", "D": "Enable PHS and wait for users to authenticate via cloud naturally"},
     "correct": "B",
     "explanation": ("Staged Rollout keeps the domain federated while specific pilot users authenticate via "
                      "PHS instead of AD FS -- rollback is just removing them from the pilot group. Domain "
                      "conversion (A) is not reversible in the short term. PHS alone (D) doesn't move users off AD FS while the domain stays federated."),
     "pattern_refs": ["Staged Rollout != domain conversion -- rollout tests, conversion commits"]},

    {"id": "CS6-Q3", "case_study": "CS6", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies BR3 and SR3 -- factory workers on domain-joined PCs get NO MFA prompt on-site (without disabling MFA)?",
     "options": {"A": "CA named location for factory IPs, exclude factory workers from MFA", "B": "Configure Seamless SSO and deploy the required GPO to domain-joined factory PCs",
                 "C": "Disable MFA for the factory worker group entirely", "D": "Configure WHfB on all factory PCs"},
     "correct": "B",
     "explanation": ("Seamless SSO uses Kerberos to authenticate silently -- the Windows login IS the Entra sign-in, "
                      "satisfying MFA transparently rather than removing it. A and C both strip the MFA requirement "
                      "outright -- a security regression. WHfB (D) needs per-user enrollment, incompatible with shared PCs."),
     "pattern_refs": ["Seamless SSO satisfies MFA transparently -- never disable MFA"]},

    {"id": "CS6-Q4", "case_study": "CS6", "domain": "1", "difficulty": "advanced",
     "question": "Which step must be completed FIRST in the migration sequence per TR3 (PHS -> Seamless SSO -> Staged Rollout -> apps -> convert -> decommission)?",
     "options": {"A": "Run the AD FS Application Activity report", "B": "Configure Staged Rollout with a pilot group",
                 "C": "Enable Password Hash Sync in Entra Connect", "D": "Configure Seamless SSO in Entra Connect"},
     "correct": "C",
     "explanation": ("Enabling PHS is the foundation everything else depends on -- Seamless SSO and Staged "
                      "Rollout both require PHS (or PTA) as the underlying authentication method before they can be configured."),
     "pattern_refs": ["Migration sequence: PHS -> SSO -> Staged Rollout -> Apps -> Convert -> Decommission"]},

    {"id": "CS6-Q5", "case_study": "CS6", "domain": "1", "difficulty": "intermediate",
     "question": "Which app should be migrated to Entra ID FIRST based on SR5 (activity report) and migration readiness?",
     "options": {"A": "App 8 (SAP ERP -- Low readiness) first, highest business value", "B": "Apps 1-4 (SAML 2.0 -- High readiness) first",
                 "C": "Apps 9-12 (WS-Federation) migrated together as a batch", "D": "Migrate all 12 apps simultaneously"},
     "correct": "B",
     "explanation": ("Start simple, build process confidence, and keep failures low-impact. SAP (A) has the "
                      "highest business impact if migration fails -- always saved for last. Batch (C) and "
                      "simultaneous (D) migration both multiply blast radius if something breaks, violating BR1 (no disruption)."),
     "pattern_refs": ["Start simple in app migration -- lowest complexity first, highest-impact app last"]},

    {"id": "CS6-Q6", "case_study": "CS6", "domain": "1", "difficulty": "intermediate",
     "question": "Which action must be completed BEFORE enabling SSPR for all 12,000 users, per TR4?",
     "options": {"A": "Convert all three domains from federated to managed", "B": "Enable Password Writeback in Entra Connect",
                 "C": "Decommission the AD FS farm", "D": "Migrate all legacy applications to Entra ID SSO"},
     "correct": "B",
     "explanation": ("Without writeback, an SSPR reset only updates the cloud password -- the on-prem AD password "
                      "stays unchanged and users are still locked out of domain-joined systems, generating more "
                      "helpdesk calls than it saves."),
     "pattern_refs": ["Writeback before SSPR in hybrid environments"]},

    {"id": "CS6-Q7", "case_study": "CS6", "domain": "1", "difficulty": "advanced",
     "question": "When is it safe to convert the domains from federated to managed, per BR2 and TR3?",
     "options": {"A": "After enabling PHS", "B": "After completing Staged Rollout with the pilot group",
                 "C": "After ALL 12 legacy applications have been migrated to Entra ID SSO", "D": "After the AD FS farm has been decommissioned"},
     "correct": "C",
     "explanation": ("Converting the domain moves authentication from AD FS to Entra ID -- any app still pointing "
                      "to AD FS as its IdP breaks immediately. All 12 apps must be on Entra ID first. D is "
                      "impossible -- you can't decommission AD FS while the domain is still federated to it."),
     "pattern_refs": ["Domain conversion only after all dependent apps are migrated"]},

    {"id": "CS6-Q8", "case_study": "CS6", "domain": "1", "difficulty": "intermediate",
     "question": "Which Entra Connect configuration satisfies TR2 -- must NOT be installed on a domain controller?",
     "options": {"A": "Install on the primary domain controller for best performance", "B": "Dedicated Windows Server member server with line-of-sight to at least one DC",
                 "C": "Install on the AD FS primary federation server", "D": "Entra Connect Cloud Sync agents on each domain controller"},
     "correct": "B",
     "explanation": ("A dedicated member server is the Microsoft-supported configuration -- DC compromise would "
                      "mean complete identity infrastructure compromise if Connect ran there. C also isn't "
                      "supported. D is a different product (Cloud Sync) than what's actually deployed here (full Connect Sync)."),
     "pattern_refs": ["Entra Connect: NOT on domain controller -- dedicated member server required"]},

    # ============================== CS7 -- TailwindTraders ===================
    {"id": "CS7-Q1", "case_study": "CS7", "domain": "3", "difficulty": "intermediate",
     "question": "Which solution satisfies TR1 and SR1 for the InventoryAPI Azure Function -- eliminate the hardcoded service account password?",
     "options": {"A": "App registration with a client certificate instead of a secret", "B": "Store the service account password in Key Vault instead of app settings",
                 "C": "System-Assigned Managed Identity on the Function, granted Azure SQL access", "D": "Dedicated service principal with a client secret in Key Vault"},
     "correct": "C",
     "explanation": ("TR1 requires Managed Identity for Azure-hosted workloads -- no credentials at all. Key "
                      "Vault (B, D) is the answer for secrets that CAN'T use Managed Identity, but this Function "
                      "can, so TR1 applies over TR2. A certificate (A) is still a credential requiring management."),
     "pattern_refs": ["Azure-hosted workload = Managed Identity. Cannot use MI = Key Vault. Never hardcode secrets"]},

    {"id": "CS7-Q2", "case_study": "CS7", "domain": "3", "difficulty": "intermediate",
     "question": "Which API permission type satisfies SR4 for CustomerPortal -- access only the CURRENTLY signed-in customer's data?",
     "options": {"A": "Application: User.Read.All (all profiles)", "B": "Delegated: User.Read (signed-in user's profile only)",
                 "C": "Application: User.Read", "D": "Delegated: User.ReadWrite.All"},
     "correct": "B",
     "explanation": ("Delegated permissions scope access to what the signed-in user can access -- exactly the "
                      "signed-in customer, nothing more. Application permissions (A, C) act tenant-wide regardless "
                      "of user context. D grants write access to all profiles -- massively over-privileged for a read-only need."),
     "pattern_refs": ["Delegated = user signs in and acts for them. Application = background service, no user"]},

    {"id": "CS7-Q3", "case_study": "CS7", "domain": "3", "difficulty": "intermediate",
     "question": "Which solution satisfies TR4 and BR3 -- remote access to LegacyWarehouse (on-prem IIS, cannot be modified) without VPN?",
     "options": {"A": "GSA Private Access with an application segment", "B": "Microsoft Entra Application Proxy",
                 "C": "Migrate LegacyWarehouse to Azure App Service", "D": "Custom Azure reverse proxy"},
     "correct": "B",
     "explanation": ("App Proxy is purpose-built for exactly this: unmodifiable on-prem web apps needing remote "
                      "access without a client, via a connector using outbound-only connections. TR4 explicitly "
                      "names it. Migrating the app (C) violates 'no modification'."),
     "pattern_refs": ["App Proxy = on-premises web app, no client needed. GSA = any protocol, needs client"]},

    {"id": "CS7-Q4", "case_study": "CS7", "domain": "3", "difficulty": "advanced",
     "question": "Which Graph API permission satisfies TR5 and SR3 for HR Sync App -- minimum permission to create, update, and disable users (background service, no user context)?",
     "options": {"A": "Delegated: User.ReadWrite.All", "B": "Application: Global Reader",
                 "C": "Application: User.ReadWrite.All", "D": "Application: Directory.ReadWrite.All"},
     "correct": "C",
     "explanation": ("Background service = Application permission (Delegated requires a signed-in user, which a "
                      "sync service doesn't have). User.ReadWrite.All is exactly sufficient for user CRUD. "
                      "Directory.ReadWrite.All (D) is massively over-scoped -- it also covers groups, apps, roles, policies."),
     "pattern_refs": ["User.ReadWrite.All != Directory.ReadWrite.All -- always choose narrowest scope"]},

    {"id": "CS7-Q5", "case_study": "CS7", "domain": "3", "difficulty": "intermediate",
     "question": "Which solution satisfies TR3 and BR2 -- automated Salesforce provisioning AND deprovisioning?",
     "options": {"A": "Graph API creating Salesforce accounts on Entra user creation", "B": "SCIM 2.0 provisioning for the Salesforce enterprise application",
                 "C": "Lifecycle Workflow calling the Salesforce API on join/leave", "D": "Password-based SSO with manual account management"},
     "correct": "B",
     "explanation": ("Salesforce is a gallery app with native SCIM support in Entra -- TR3 requires SCIM "
                      "explicitly. Graph API (A) manages Entra users, not Salesforce accounts directly. A custom "
                      "Lifecycle Workflow integration (C) is exactly the custom solution TR3 rules out."),
     "pattern_refs": ["SCIM = the answer for SaaS gallery app provisioning"]},

    {"id": "CS7-Q6", "case_study": "CS7", "domain": "3", "difficulty": "advanced",
     "question": "Which solution satisfies TR2 and BR5 for the ReportingService client secret -- automated rotation, secret never in source code?",
     "options": {"A": "Environment variable on the Azure VM", "B": "Azure Key Vault with automatic rotation, referenced via Key Vault reference",
                 "C": "Client certificate stored on the VM", "D": "Managed Identity, removing the secret entirely"},
     "correct": "B",
     "explanation": ("TR2 (Key Vault for secrets that can't use Managed Identity) and BR5 (automated rotation) "
                      "point to Key Vault as the tested answer. Environment variables (A) still count as config, "
                      "which SR2 rules out. Note: D would technically be the strongest fix since the VM could use MI instead -- but the question is testing TR2/BR5 specifically."),
     "pattern_refs": ["Azure-hosted = Managed Identity where possible. Cannot use MI = Key Vault with rotation"]},

    {"id": "CS7-Q7", "case_study": "CS7", "domain": "3", "difficulty": "intermediate",
     "question": "Which solution satisfies SR5 -- admin consent only for permissions that are actively used (8 apps have unused consented permissions)?",
     "options": {"A": "Review all app registrations, remove unused permissions, re-grant consent only for what's needed", "B": "Disable admin consent for all applications entirely",
                 "C": "Require admin approval for all future permission requests only", "D": "Enable the admin consent workflow for users to request consent"},
     "correct": "A",
     "explanation": ("This is a remediation question -- the 8 apps need their existing over-consented permissions "
                      "actually revoked and re-granted at the correct scope, today. Options C and D only affect "
                      "future requests and don't touch the 8 existing over-privileged apps."),
     "pattern_refs": ["Remediate existing over-consent -- don't just gate future requests"]},

    {"id": "CS7-Q8", "case_study": "CS7", "domain": "3", "difficulty": "advanced",
     "question": "Which solution satisfies SR6 and TR6 -- monitor workload identity risk for anomalous service principal behaviour?",
     "options": {"A": "Standard ID Protection user risk policies applied to service principals", "B": "Workload Identities Premium with workload identity risk policies in ID Protection",
                 "C": "Sentinel KQL queries detecting unusual sign-in patterns", "D": "CA policies targeting service principals with sign-in risk conditions"},
     "correct": "B",
     "explanation": ("TR6 explicitly names Workload Identities Premium, which is already licensed in this "
                      "environment. Standard ID Protection (A) targets user accounts, not service principals -- "
                      "different feature entirely. D's sign-in risk conditions for workload identities have no data to act on without the Premium licence generating them."),
     "pattern_refs": ["Workload Identities Premium = separate licence for service principal risk monitoring"]},

    # ============================== CS8 -- BlueSky Media Group ===============
    {"id": "CS8-Q1", "case_study": "CS8", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies BR1 and SR3 -- block contractors from Copilot, allow permanent staff, using CA policy not just licence removal?",
     "options": {"A": "Remove the Copilot licence from all contractor accounts", "B": "CA policy targeting guest users, Microsoft Copilot as the target resource, Grant = Block",
                 "C": "Disable Copilot for guests in the M365 admin centre", "D": "Remove contractors from all M365 groups"},
     "correct": "B",
     "explanation": ("TR4 explicitly requires CA policy, not licence removal alone -- CA is the auditable, "
                      "enforceable identity governance layer. C's global setting can't distinguish guests from "
                      "staff. D doesn't actually control Copilot access, which runs on licence + CA, not group membership."),
     "pattern_refs": ["Block Copilot for guests = CA policy targeting Copilot app"]},

    {"id": "CS8-Q2", "case_study": "CS8", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies BR2 and SR4 -- AI Acceptable Use Policy accepted before FIRST Copilot use, via CA not self-service?",
     "options": {"A": "Email the policy, require reply confirmation", "B": "Onboarding portal acceptance checkbox",
                 "C": "Terms of Use policy (PDF) enforced via CA policy targeting Microsoft Copilot", "D": "Copilot displays policy text on first launch via admin centre"},
     "correct": "C",
     "explanation": ("Same pattern as any ToU requirement -- configured in Identity Governance, enforced via CA. "
                      "SR4 explicitly rules out self-service acknowledgement (A, B), neither of which are "
                      "auditable in Entra or prevent access if incomplete."),
     "pattern_refs": ["ToU = CA enforcement not manual -- PDF format required"]},

    {"id": "CS8-Q3", "case_study": "CS8", "domain": "4", "difficulty": "advanced",
     "question": "Which solution satisfies BR3, SR2, and TR2 -- prevent Copilot from surfacing strictly confidential content, using sensitivity labels not CA?",
     "options": {"A": "CA policy blocking access to SharePoint sites with confidential documents", "B": "Purview sensitivity labels, 'Strictly Confidential' applied to protected documents",
                 "C": "Remove all user permissions to strictly confidential sites", "D": "Configure Copilot to only search approved SharePoint sites"},
     "correct": "B",
     "explanation": ("TR2 explicitly requires sensitivity labels, not CA. Labels travel with the document and "
                      "restrict what Copilot can include in outputs even if the user technically has read access. "
                      "A contradicts TR2 directly. D isn't a real Copilot configuration option -- labels are the supported mechanism."),
     "pattern_refs": ["Copilot content protection = sensitivity labels NOT CA policies"]},

    {"id": "CS8-Q4", "case_study": "CS8", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies SR5 and TR3 -- block shadow AI (personal ChatGPT etc.) on corporate networks, using GSA not DNS?",
     "options": {"A": "CA policy blocking access to chatgpt.com and similar domains", "B": "DNS filtering at the corporate DNS server",
                 "C": "GSA Internet Access with web content filtering blocking the AI services category", "D": "An HR policy requiring staff not to use personal AI tools"},
     "correct": "C",
     "explanation": ("TR3 explicitly requires GSA Internet Access. CA (A) can't block arbitrary internet domains, "
                      "only Entra-registered apps. DNS (B) is explicitly ruled out and easily bypassed. A written "
                      "policy (D) isn't a technical network-level control."),
     "pattern_refs": ["Shadow AI blocking = GSA Internet Access web filter not DNS not CA"]},

    {"id": "CS8-Q5", "case_study": "CS8", "domain": "4", "difficulty": "advanced",
     "question": "Which solution satisfies BR5 and TR5 -- freelance talent verify identity digitally for contract signing, without creating Microsoft accounts?",
     "options": {"A": "B2B guest accounts requiring sign-in to verify identity", "B": "Microsoft Entra Verified ID -- issue verifiable credentials presented digitally",
                 "C": "DocuSign identity verification integrated with SharePoint", "D": "In-person identity verification at BlueSky offices"},
     "correct": "B",
     "explanation": ("Verified ID is decentralised -- talent hold a credential in their Authenticator wallet and "
                      "never sign in to BlueSky's tenant at all, satisfying TR5's no-Microsoft-account requirement "
                      "precisely. B2B guests (A) still require account creation/redemption."),
     "pattern_refs": ["Verified ID = no Microsoft account needed, decentralised, Authenticator wallet"]},

    {"id": "CS8-Q6", "case_study": "CS8", "domain": "4", "difficulty": "advanced",
     "question": "Which solution addresses SR1 -- the ROOT CAUSE of Incident 1 (a user inheriting stale SharePoint access that Copilot then summarised)?",
     "options": {"A": "Deploy sensitivity labels to all documents so Copilot cannot access any content", "B": "Disable Copilot for all users until permissions are reviewed",
                 "C": "Access Reviews targeting SharePoint site membership to identify and remove unnecessary access", "D": "CA policy requiring MFA for all SharePoint access"},
     "correct": "C",
     "explanation": ("Copilot inherits user permissions -- the fix is fixing the permissions, not the Copilot "
                      "layer. Access Reviews directly remediate the stale group membership that caused the "
                      "incident. Labels (A) address what Copilot outputs, not who has underlying access. MFA (D) doesn't reduce permissions at all."),
     "pattern_refs": ["Copilot inherits user permissions -- fix permissions not Copilot"]},

    {"id": "CS8-Q7", "case_study": "CS8", "domain": "4", "difficulty": "intermediate",
     "question": "Which solution satisfies BR6 and TR6 -- audit all Copilot interactions including prompts and content surfaced?",
     "options": {"A": "Entra ID sign-in logs filtered by Copilot", "B": "Diagnostic settings exporting Copilot activity to Log Analytics",
                 "C": "Microsoft Purview audit logs -- search for Copilot interaction events", "D": "Microsoft Sentinel alerts for Copilot usage patterns"},
     "correct": "C",
     "explanation": ("TR6 explicitly states Copilot audit lives in Purview, not Entra. Sign-in logs (A) and "
                      "diagnostic exports of Entra logs (B) only show authentication events -- not prompts or "
                      "content sources, which is what BR6 requires."),
     "pattern_refs": ["Copilot audit = Purview audit logs NOT Entra sign-in logs"]},

    {"id": "CS8-Q8", "case_study": "CS8", "domain": "4", "difficulty": "intermediate",
     "question": "PRINCIPLE QUESTION: An over-privileged staff member uses Copilot to access sensitive content. What explains this and what is the PRIMARY fix?",
     "options": {"A": "Copilot has a security vulnerability -- report to Microsoft, disable Copilot", "B": "Copilot inherits the user's permissions -- fix is reducing permissions via Access Reviews and least privilege",
                 "C": "Copilot needs its own separate permission set from the user", "D": "The sensitivity label failed -- re-apply all labels"},
     "correct": "B",
     "explanation": ("Copilot inherits the signed-in user's permissions exactly, nothing more -- this is working "
                      "as designed, not a vulnerability (A). Copilot has no separate permission model of its own "
                      "(C). If a document was never labelled, that's a labelling gap, not a label 'failure' (D) -- and it's a secondary control, not the primary fix."),
     "pattern_refs": ["Copilot inherits user permissions -- fix permissions not Copilot"]},

    # ============================== CS9 -- Woodgrove Health Network ==========
    {"id": "CS9-Q1", "case_study": "CS9", "domain": "4", "difficulty": "advanced",
     "question": "Which reviewer configuration satisfies TR1 and SR1 for the 2,800-account clinical system access review (self-review not acceptable, auto-remove on no response)?",
     "options": {"A": "Self-review -- each user confirms their own access", "B": "Manager review with fallback reviewers, auto-apply, no response = Remove access",
                 "C": "Resource owner review by clinical system administrators", "D": "Single reviewer -- the CISO reviews all 2,800 accounts"},
     "correct": "B",
     "explanation": ("Managers have business context and reviews scale in parallel across 2,800 accounts. "
                      "Fallback reviewers matter -- if a manager has left, the review would otherwise be "
                      "abandoned and access would persist. Self-review (A) is a conflict of interest, explicitly ruled out. A single reviewer (D) can't realistically process 2,800 accounts in 30 days."),
     "pattern_refs": ["Access Reviews fallback reviewers always required at scale"]},

    {"id": "CS9-Q2", "case_study": "CS9", "domain": "4", "difficulty": "intermediate",
     "question": "Which configuration satisfies BR3 and SR2 -- specialist referral users self-request access that expires after 90 days, no standing access?",
     "options": {"A": "Security group with a 90-day group expiry", "B": "Connected Organization + access package with 90-day expiry, Renewal allowed = No",
                 "C": "B2B invitations with manual 90-day tracking", "D": "Lifecycle Workflow triggered by referral start date"},
     "correct": "B",
     "explanation": ("Connected Organization enables self-service requests; the access package's hard 90-day "
                      "expiry with no renewal satisfies 'no standing access'. Manual tracking (C) doesn't scale to "
                      "180 high-turnover users. Lifecycle Workflows (D) govern internal users, not B2B guest package assignments."),
     "pattern_refs": ["Connected Organizations must be configured before external users can request access packages"]},

    {"id": "CS9-Q3", "case_study": "CS9", "domain": "2", "difficulty": "intermediate",
     "question": "Which solution satisfies SR3, BR4, and TR3 -- filter clinical device internet access (social media, streaming, personal cloud), using GSA not proxy?",
     "options": {"A": "On-premises proxy server with URL filtering", "B": "CA policies blocking social media and streaming apps registered in Entra",
                 "C": "GSA Internet Access with a web content filtering policy", "D": "DNS filtering on the clinical network"},
     "correct": "C",
     "explanation": ("TR3 explicitly requires GSA Internet Access. An on-prem proxy (A) only filters traffic on "
                      "the corporate network, missing off-site clinical devices. CA (B) can't block arbitrary "
                      "internet sites like Netflix or Facebook, only Entra-registered apps."),
     "pattern_refs": ["Shadow AI / web filtering = GSA Internet Access not CA not DNS"]},

    {"id": "CS9-Q4", "case_study": "CS9", "domain": "2", "difficulty": "advanced",
     "question": "Which KQL query correctly detects impossible travel (sign-in from 2+ countries within 1 hour), per TR4 (SignInLogs for auth events)?",
     "options": {"A": "AuditLogs, dcount(InitiatedBy) by UserDisplayName", "B": "SignInLogs, extend Country from LocationDetails, summarize dcount(Country) by UserPrincipalName, where Countries >= 2",
                 "C": "SignInLogs where RiskEventTypes contains 'impossibleTravel'", "D": "AuditLogs where Category == 'SignInLogs'"},
     "correct": "B",
     "explanation": ("Impossible travel is an authentication event -- SignInLogs is the correct table, with "
                      "country extracted from LocationDetails and a distinct-country count per user. AuditLogs "
                      "(A, D) are for directory changes, not sign-in patterns, and D's syntax doesn't actually work that way."),
     "pattern_refs": ["SignInLogs = authentication events. AuditLogs = directory changes"]},

    {"id": "CS9-Q5", "case_study": "CS9", "domain": "4", "difficulty": "intermediate",
     "question": "Which three actions, in the correct ORDER, will most improve the Identity Secure Score per BR5 (61 -> 80+)?",
     "options": {"A": "1. Enable SSPR 2. MFA for admins 3. Disable stale accounts", "B": "1. MFA for admins (CA) 2. Enable SSPR 3. Disable stale accounts (Lifecycle Workflow)",
                 "C": "1. Disable stale accounts 2. Enable SSPR 3. MFA for admins", "D": "1. MFA for admins 2. Disable stale accounts 3. Configure access reviews"},
     "correct": "B",
     "explanation": ("MFA for admins always comes first -- it protects the accounts that will configure "
                      "everything else and has the highest single score impact. SSPR needs admin MFA in place "
                      "first for safe configuration. Doing anything before securing admin accounts (A, C) leaves them exposed during the rest of the work."),
     "pattern_refs": ["Secure Score order: MFA admins first -> SSPR -> stale accounts"]},

    {"id": "CS9-Q6", "case_study": "CS9", "domain": "4", "difficulty": "advanced",
     "question": "Which KQL query detects privileged role activation outside business hours per SR4?",
     "options": {"A": "SignInLogs where AppDisplayName == 'PIM', hourofday !between (8..18)", "B": "AuditLogs where OperationName == 'Add member to role', hourofday !between (8..18)",
                 "C": "SignInLogs where RiskLevel == 'high', AppDisplayName contains 'Admin'", "D": "AuditLogs where Category == 'RoleManagement', last 24h, no time filter"},
     "correct": "B",
     "explanation": ("Role activation is a directory CHANGE, not an authentication event -- AuditLogs is correct, "
                      "filtered on the specific PIM-activation operation name and an explicit outside-hours "
                      "window. A queries the wrong table entirely. D has no time filter, so it doesn't satisfy 'outside business hours'."),
     "pattern_refs": ["SignInLogs = auth events. AuditLogs = directory changes"]},

    {"id": "CS9-Q7", "case_study": "CS9", "domain": "1", "difficulty": "intermediate",
     "question": "Which solution satisfies SR5 -- automatically disable accounts inactive for 90+ days?",
     "options": {"A": "Monthly PowerShell script identifying and disabling inactive accounts", "B": "Access Review targeting all users, auto-apply, 90-day recurrence",
                 "C": "Lifecycle Workflow with an attribute-based trigger on lastSignInDateTime > 90 days", "D": "CA policy blocking sign-in after 90 days inactivity"},
     "correct": "C",
     "explanation": ("Lifecycle Workflow fires automatically on the attribute condition -- no scheduling or "
                      "human decision required. A script (A) still needs scheduling/execution. Access Review (B) "
                      "requires a human reviewer response. CA (D) can't evaluate lastSignInDateTime as a condition -- it isn't an available CA attribute."),
     "pattern_refs": ["Lifecycle Workflow for automatic inactivity disable. Access Review needs a human"]},

    {"id": "CS9-Q8", "case_study": "CS9", "domain": "4", "difficulty": "advanced",
     "question": "Which configuration satisfies BR6 -- complete audit trail for EMR access INCLUDING who approved access and when (not just who signed in)?",
     "options": {"A": "AuditLogs exported to Log Analytics, filtered by EMR application", "B": "Access packages with approval workflows + Entitlement Management audit reports",
                 "C": "CA policy for EMR requiring MFA -- sign-in logs show all access attempts", "D": "Sentinel workbook showing EMR sign-in activity"},
     "correct": "B",
     "explanation": ("BR6 specifically needs the approval chain -- who approved, when, what justification -- which "
                      "only Entitlement Management's audit reports capture. AuditLogs (A), CA/sign-in logs (C), "
                      "and Sentinel workbooks (D) all show WHO ACCESSED, not who approved the request in the first place."),
     "pattern_refs": ["Entitlement audit = who approved. Sign-in logs = who accessed"]},

    # ============================== CS10 -- Meridian Group (Final Boss) ======
    {"id": "CS10-Q1", "case_study": "CS10", "domain": "1", "difficulty": "final_boss",
     "question": "[DOMAIN 1] Which solution satisfies BR1 and TR1 -- TechVentures' 2,800 staff appear as internal users in Meridian without individual invitations?",
     "options": {"A": "B2B invitations to all 2,800 individually", "B": "Cross-Tenant Synchronization from TechVentures to Meridian",
                 "C": "Internal member accounts for all 2,800", "D": "Connected Organizations + access packages"},
     "correct": "B",
     "explanation": ("Acquisition scenario -- cross-tenant sync provisions internal-looking members automatically "
                      "at scale, matching the identical pattern from CS3 Q1 and CS5 Q8. Access packages (D) create "
                      "guest access, not the internal appearance BR1 requires."),
     "pattern_refs": ["Cross-tenant sync = internal/acquisition appearance"]},

    {"id": "CS10-Q2", "case_study": "CS10", "domain": "1", "difficulty": "final_boss",
     "question": "[DOMAIN 1] Which solution satisfies SR7 and BR2 -- former employee account disabled within 1 HOUR automatically, triggered on employeeLeaveDateTime?",
     "options": {"A": "Daily PowerShell script disabling terminated accounts", "B": "Weekly Access Review with auto-apply",
                 "C": "Leaver Lifecycle Workflow triggered on employeeLeaveDateTime with a Disable account task", "D": "CA policy blocking sign-in for terminated accounts"},
     "correct": "C",
     "explanation": ("Lifecycle Workflows fire within 30-60 minutes of the trigger attribute being set -- the "
                      "only option meeting a 1-hour bar. A daily script (A) or weekly review (B) both leave far "
                      "too large a window, which is exactly what caused the original 6-month exposure. CA (D) can't query HR termination status as a condition."),
     "pattern_refs": ["Lifecycle Workflow trigger = employeeLeaveDateTime for leavers"]},

    {"id": "CS10-Q3", "case_study": "CS10", "domain": "2", "difficulty": "final_boss",
     "question": "[DOMAIN 2] Which solution satisfies SR1 AND SR4 simultaneously -- prevent MFA fatigue for staff AND move contractors off SMS?",
     "options": {"A": "Number matching for staff + Authenticator for contractors (SMS disabled)", "B": "Deploy FIDO2 to all staff and contractors",
                 "C": "Number matching for staff, keep SMS for contractors", "D": "Certificate-based auth for everyone using existing PKI"},
     "correct": "A",
     "explanation": ("Two separate requirements, two separate fixes in one option: number matching stops fatigue "
                      "for staff, and disabling SMS in favour of Authenticator for contractors satisfies SR4 "
                      "within their existing P1 licence. FIDO2 for all 4,000 contractors (B) is impractical at that scale on unmanaged devices. C explicitly violates SR4."),
     "pattern_refs": ["Number matching prevents MFA fatigue but is not phishing-resistant"]},

    {"id": "CS10-Q4", "case_study": "CS10", "domain": "2", "difficulty": "final_boss",
     "question": "[DOMAIN 2] Which solution satisfies SR3 and TR6 -- HIGH risk sign-ins automatically blocked, modern CA approach (not legacy ID Protection portal)?",
     "options": {"A": "ID Protection Sign-in risk policy blocking High risk", "B": "CA policy: Sign-in risk = High > Grant = Block access",
                 "C": "Sentinel alert on High risk sign-ins", "D": "Security Defaults 'Require MFA for risky sign-ins'"},
     "correct": "B",
     "explanation": ("Identical pattern to CS2 Q1 -- TR6 rules out the legacy portal (A) explicitly. C is reactive, "
                      "not automatic blocking. Security Defaults (D) can't coexist with the existing CA policies already in place."),
     "pattern_refs": ["Legacy ID Protection portal = wrong when TR says modern CA approach"]},

    {"id": "CS10-Q5", "case_study": "CS10", "domain": "3", "difficulty": "final_boss",
     "question": "[DOMAIN 3] Which solution satisfies BR6 and TR4 -- eliminate hardcoded credentials from the 23 Azure apps found exposed on GitHub?",
     "options": {"A": "Rotate all secrets, store in environment variables", "B": "Managed Identities for Azure-hosted apps; Key Vault for non-Azure apps",
                 "C": "Client certificates on application servers", "D": "Azure DevOps pipeline variables"},
     "correct": "B",
     "explanation": ("The Managed Identity hierarchy from CS7: Azure-hosted -> Managed Identity (no credential at "
                      "all); can't use MI -> Key Vault. Environment variables (A) are still config, which the "
                      "incident's root cause (secrets in source control) explicitly rules out. Pipeline variables (D) aren't readable by apps at runtime."),
     "pattern_refs": ["Azure-hosted workload = Managed Identity. Cannot use MI = Key Vault. Never hardcode secrets"]},

    {"id": "CS10-Q6", "case_study": "CS10", "domain": "4", "difficulty": "final_boss",
     "question": "[DOMAIN 4] Which solution satisfies SR2 and SR6 -- convert Global Admins to PIM with correct break-glass and activation settings?",
     "options": {"A": "All 8 GAs eligible, 8hr max, no approval", "B": "6 GAs eligible (justification + MFA + 4hr max + approval) + 2 permanent break-glass excluded from all CA",
                 "C": "All 8 GAs eligible, approval required for all", "D": "Keep 4 permanent, convert 4 to eligible"},
     "correct": "B",
     "explanation": ("Exactly 2 permanent break-glass (never more, never zero) plus the remaining GAs on PIM "
                      "eligible with the specific 4-hour cap SR6 states. A's 8 hours violates SR6. C converts "
                      "break-glass to eligible too, which defeats its purpose -- break-glass must stay permanent to work if PIM itself is unavailable. D's 4 permanent violates SR2's cap of 2."),
     "pattern_refs": ["PIM: break-glass = exactly 2, permanent, excluded from all CA, monitored 24/7"]},

    {"id": "CS10-Q7", "case_study": "CS10", "domain": "2+4", "difficulty": "final_boss",
     "question": "[DOMAIN 2+4] Which solution satisfies BR3, BR5, and TR5 simultaneously -- block contractors from Copilot AND protect privileged legal documents from Copilot?",
     "options": {"A": "Remove contractor Copilot licence + CA policy blocking SharePoint for legal staff", "B": "CA policy blocking contractors from Copilot + Purview sensitivity labels on legal documents",
                 "C": "Remove contractors from all M365 groups + label all documents", "D": "Disable Copilot tenant-wide until labels are deployed"},
     "correct": "B",
     "explanation": ("Two distinct requirements need two distinct controls: CA policy for the contractor block "
                      "(CS8 Q1 pattern) and sensitivity labels for content protection (CS8 Q3 pattern) -- TR5 "
                      "explicitly says labels not CA for the document side. A blocks legal staff from their own documents, the wrong direction entirely."),
     "pattern_refs": ["Block Copilot for guests = CA policy. Copilot content protection = sensitivity labels"]},

    {"id": "CS10-Q8", "case_study": "CS10", "domain": "2", "difficulty": "final_boss",
     "question": "[DOMAIN 2] Which solution satisfies SR5 and TR7 -- block personal cloud storage at network level for ALL corporate devices, using GSA not DNS?",
     "options": {"A": "CA policies blocking OneDrive personal, Google Drive, Dropbox", "B": "DNS filtering on the corporate network",
                 "C": "GSA Internet Access with web content filtering blocking the personal cloud storage category", "D": "Purview DLP policy blocking uploads to personal cloud storage"},
     "correct": "C",
     "explanation": ("Third appearance of this exact pattern (after CS8 Q4 and CS9 Q3) -- CA (A) can only govern "
                      "Entra-registered apps, not arbitrary personal cloud services. TR7 explicitly rules out DNS "
                      "(B). DLP (D) protects content leaving, but doesn't block the destination at the network level for all traffic."),
     "pattern_refs": ["Shadow AI / web filtering = GSA Internet Access not CA not DNS"]},
]

# --------------------------------------------------------------------------
# COMPLETE PATTERN LIBRARY -- 50 patterns distilled across all 10 case studies,
# colour-coded by domain in the original CS10 material (D1 blue / D2 green /
# D3 purple / D4 amber). Kept here as plain domain tags for lookup.
# --------------------------------------------------------------------------

PATTERN_LIBRARY = [
    {"domain": "1", "pattern": "Legacy ID Protection portal = wrong when TR says modern CA approach", "sources": ["CS1", "CS2", "CS10"]},
    {"domain": "1", "pattern": "Disable before delete -- never immediate deletion", "sources": ["CS2", "CS3", "CS5", "CS6", "CS9"]},
    {"domain": "1", "pattern": "Check existing licences before assuming a purchase is needed", "sources": ["CS2", "CS3", "CS4", "CS5", "CS6", "CS7", "CS8", "CS9", "CS10"]},
    {"domain": "1", "pattern": "Cross-tenant sync = internal/acquisition appearance. B2B = partners/guests. External ID = consumers", "sources": ["CS3", "CS5", "CS10"]},
    {"domain": "1", "pattern": "SCIM over CSV for HR and SaaS provisioning -- always", "sources": ["CS5", "CS7", "CS9"]},
    {"domain": "1", "pattern": "Scale eliminates manual solutions -- any manual answer fails at thousands of users", "sources": ["CS5", "CS9"]},
    {"domain": "1", "pattern": "Lifecycle Workflow trigger = employeeLeaveDateTime for leavers. Offset -1/-2 for joiners", "sources": ["CS5", "CS6", "CS10"]},
    {"domain": "1", "pattern": "Mover Lifecycle Workflow must REMOVE old access BEFORE assigning new -- privilege creep prevention", "sources": ["CS5"]},
    {"domain": "1", "pattern": "Dynamic groups alone don't prevent privilege creep -- Lifecycle Workflow remove-first needed", "sources": ["CS5"]},
    {"domain": "1", "pattern": "PHS preferred over PTA -- enables ID Protection leaked-credential detection + cloud resilience", "sources": ["CS6"]},
    {"domain": "1", "pattern": "Migration sequence: PHS -> Seamless SSO -> Staged Rollout -> Migrate apps -> Convert domain -> Decommission AD FS", "sources": ["CS6"]},
    {"domain": "1", "pattern": "Staged Rollout != domain conversion -- Staged Rollout tests with domain still federated", "sources": ["CS6"]},
    {"domain": "1", "pattern": "Password Writeback must be enabled BEFORE SSPR in hybrid environments", "sources": ["CS6"]},
    {"domain": "1", "pattern": "Entra Connect: NOT on domain controller -- dedicated member server required", "sources": ["CS6"]},
    {"domain": "2", "pattern": "MFA regardless of home tenant = CA policy with NO cross-tenant MFA trust", "sources": ["CS2", "CS3", "CS4", "CS9"]},
    {"domain": "2", "pattern": "Number matching prevents MFA fatigue but is NOT phishing-resistant", "sources": ["CS4", "CS10"]},
    {"domain": "2", "pattern": "Phishing-resistant MFA = FIDO2 / WHfB / CBA only -- Authenticator is NOT phishing-resistant", "sources": ["CS4"]},
    {"domain": "2", "pattern": "Authentication Strength: phishing-resistant != Require MFA (any method)", "sources": ["CS4"]},
    {"domain": "2", "pattern": "GSA connector = outbound HTTPS ONLY -- no inbound firewall rules required", "sources": ["CS4"]},
    {"domain": "2", "pattern": "GSA Private Access = replaces VPN, app-by-app ZTNA", "sources": ["CS4", "CS10"]},
    {"domain": "2", "pattern": "GSA Internet Access = web content filter. Blocks categories not individual URLs. Not CA, not DNS", "sources": ["CS8", "CS9", "CS10"]},
    {"domain": "2", "pattern": "Compliant Network CA condition = enforces that users MUST go through GSA", "sources": ["CS4"]},
    {"domain": "2", "pattern": "Remote Network Connectivity = branch offices without per-device client (IPsec tunnel)", "sources": ["CS4"]},
    {"domain": "2", "pattern": "Single-factor CBA vs multi-factor CBA -- OID mapping makes CBA count as MFA", "sources": ["CS4"]},
    {"domain": "2", "pattern": "SSPR CA enforcement: unregistered users cannot sign in until registered -- not just nudged", "sources": ["CS5", "CS9"]},
    {"domain": "2", "pattern": "ToU = CA enforcement not manual acknowledgement -- PDF format required", "sources": ["CS3", "CS8"]},
    {"domain": "2", "pattern": "Risk-based CA: Sign-in risk High = Block. User risk High = Require password change", "sources": ["CS2", "CS10"]},
    {"domain": "2", "pattern": "Copilot shadow AI / web filtering = GSA Internet Access. CA cannot block arbitrary internet", "sources": ["CS8", "CS9", "CS10"]},
    {"domain": "3", "pattern": "Azure-hosted workload = Managed Identity. Cannot use MI = Key Vault. Never hardcode secrets", "sources": ["CS7", "CS10"]},
    {"domain": "3", "pattern": "Delegated permission = user signs in, app acts for them. Application permission = background service, no user", "sources": ["CS7"]},
    {"domain": "3", "pattern": "User.ReadWrite.All != Directory.ReadWrite.All -- always choose narrowest scope", "sources": ["CS7"]},
    {"domain": "3", "pattern": "SCIM 2.0 = answer for SaaS gallery app provisioning (Salesforce, ServiceNow etc.)", "sources": ["CS5", "CS7"]},
    {"domain": "3", "pattern": "App Proxy = on-premises web app, no client needed, no app modification. GSA = any protocol, needs client", "sources": ["CS7"]},
    {"domain": "3", "pattern": "Workload Identities Premium = separate licence for service principal risk monitoring", "sources": ["CS7"]},
    {"domain": "4", "pattern": "PIM: break-glass = exactly 2, permanent, .onmicrosoft.com, excluded from ALL CA, monitored 24/7", "sources": ["CS1", "CS6", "CS10"]},
    {"domain": "4", "pattern": "PIM: max activation = 4-8 hours. An SR requiring a specific number overrides the default", "sources": ["CS2", "CS4", "CS10"]},
    {"domain": "4", "pattern": "PIM: always require MFA + justification on activation for privileged roles", "sources": ["CS1", "CS2", "CS4"]},
    {"domain": "4", "pattern": "Access Reviews: auto-apply ON + no response = Remove access + fallback reviewers always", "sources": ["CS3", "CS9"]},
    {"domain": "4", "pattern": "Access Reviews: self-review NOT acceptable for sensitive/clinical/privileged access", "sources": ["CS9"]},
    {"domain": "4", "pattern": "Entitlement Management: catalog first, then resources, then access package, then policy", "sources": ["CS3", "CS9"]},
    {"domain": "4", "pattern": "Connected Organizations must be configured BEFORE external users can request access packages", "sources": ["CS3", "CS9"]},
    {"domain": "4", "pattern": "Access package hard expiry: Renewal allowed = No. No admin can extend without a new request", "sources": ["CS5", "CS9"]},
    {"domain": "4", "pattern": "Copilot inherits user permissions -- fix permissions via Access Reviews, not Copilot settings", "sources": ["CS8"]},
    {"domain": "4", "pattern": "Copilot content protection = Purview sensitivity labels NOT CA policies", "sources": ["CS8", "CS10"]},
    {"domain": "4", "pattern": "Copilot audit = Microsoft Purview audit logs NOT Entra sign-in logs", "sources": ["CS8"]},
    {"domain": "4", "pattern": "Verified ID = no Microsoft account needed, decentralised, credential in Authenticator wallet", "sources": ["CS8"]},
    {"domain": "4", "pattern": "Secure Score order: MFA for admins FIRST -> SSPR -> stale accounts", "sources": ["CS9"]},
    {"domain": "4", "pattern": "Lifecycle Workflow for automatic inactivity disable. Access Review needs a human reviewer", "sources": ["CS9"]},
    {"domain": "4", "pattern": "Entitlement Management audit = who approved + when. Sign-in logs = who accessed + when", "sources": ["CS9"]},
    {"domain": "4", "pattern": "SignInLogs = authentication events. AuditLogs = directory changes -- know which table", "sources": ["CS9"]},
]

ALL_CASE_STUDY_IDS = list(CASE_STUDY_META.keys())

# --------------------------------------------------------------------------
# CASE_STUDY_REQUIREMENTS -- full Existing Environment facts and Business/
# Security/Technical Requirements per case study, transcribed from the
# original PDFs. Questions reference these by code (e.g. "satisfies BR1
# and TR3") so students need to actually see what BR1/TR3 say, not just
# the condensed one-paragraph context above. Use display_case_study_briefing()
# or get_case_study_briefing() to surface this.
# --------------------------------------------------------------------------

CASE_STUDY_REQUIREMENTS = {

"CS1": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- hybrid (on-prem AD via Entra Connect)"),
        ("Licence", "Entra ID P2 for all staff | P1 for contractors"),
        ("Authentication", "Per-user MFA for 78% of staff -- SMS OTP only"),
        ("Legacy auth", "340 sign-ins/day still using legacy protocols"),
        ("Privileged accounts", "14 Global Administrators (permanent) -- no PIM configured"),
        ("Break-glass", "One account exists -- no monitoring configured"),
        ("Password reset", "All via helpdesk -- 180 tickets/month at NZD $18 each"),
        ("Shared workstations", "280 shared clinical workstations, shared Windows login"),
        ("External users", "180 Southern Cross partners added as internal members"),
        ("Conditional Access", "Require MFA (disabled) / Block legacy auth (report-only)"),
        ("Administrative Units", "Not configured -- helpdesk has tenant-wide User Admin"),
        ("AD FS", "AD FS 2016 farm in use for 3 legacy clinical applications"),
    ],
    "business": [
        "BR1: Clinical staff authenticate to shared ward workstations without a smartphone",
        "BR2: Password reset must not require helpdesk involvement",
        "BR3: Southern Cross partner users governed separately from internal staff",
        "BR4: Contractors must not access the ClinicalCore patient records system",
        "BR5: Helpdesk can only reset passwords for staff in their own department",
        "BR6: New clinical staff have day-one access without IT tickets",
    ],
    "security": [
        "SR1: All admin actions use phishing-resistant MFA -- SMS not acceptable",
        "SR2: No permanent standing GA access -- maximum 4 Global Admins total",
        "SR3: Legacy authentication blocked, not just monitored in report-only",
        "SR4: Break-glass accounts configured per Microsoft recommendations",
        "SR5: Privileged role activations require justification, max 4 hours",
        "SR6: ID Protection enabled with automated response to High risk sign-ins",
        "SR7: Southern Cross partners complete MFA even if home tenant enforces MFA",
    ],
    "technical": [
        "TR1: Clinical staff group membership updates automatically on HR attribute change",
        "TR2: Minimum number of Conditional Access policies possible",
        "TR3: No licence cost increase -- use existing P2/P1",
        "TR4: AD FS farm decommissioned within 6 months",
        "TR5: All changes tested in report-only mode before enforcement",
        "TR6: Minimum two authentication methods available for SSPR",
    ],
},

"CS2": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- hybrid, Entra Connect Sync running"),
        ("Licence", "Entra ID P2 permanent staff | Entra ID Free for contractors"),
        ("Password Hash Sync", "ENABLED -- PHS running and current"),
        ("ID Protection", "Enabled but no risk policies configured -- detections logged only"),
        ("Authentication", "Per-user MFA for staff -- no MFA for contractors"),
        ("Legacy auth", "Blocked -- CA policy active and enforced"),
        ("Privileged accounts", "6 Global Admins (permanent) -- PIM only for Azure resource roles"),
        ("Conditional Access", "Block legacy auth (On) / Require MFA (On) / Trusted locations (On)"),
        ("Contractor accounts", "Same OU as staff -- no attribute to distinguish them"),
        ("Stale accounts", "34 contractor accounts active with no sign-in in 180+ days"),
        ("Monitoring", "Diagnostic logs to Log Analytics -- no Sentinel alerts configured"),
        ("Insider risk", "Purview E5 licence available but Insider Risk not configured"),
        ("Named locations", "Auckland trusted | Sydney and Singapore not yet added"),
    ],
    "business": [
        "BR1: Stale contractor accounts automatically disabled after 90 days inactivity",
        "BR2: Sydney and Singapore offices get no MFA prompt on corporate networks",
        "BR3: Contractor accounts identifiable and targetable separately from staff",
        "BR4: Financial analysts blocked outside 8am-6pm NZST unless on an exception list",
        "BR5: No additional licences beyond what's currently available",
    ],
    "security": [
        "SR1: HIGH risk sign-ins automatically blocked -- manual review not acceptable",
        "SR2: HIGH risk user accounts automatically forced to reset password",
        "SR3: Impossible travel detections trigger an immediate automated response",
        "SR4: The 34 stale contractor accounts remediated immediately, prevented from recurring",
        "SR5: Insider risk signals feed into Conditional Access for medium/high risk users",
        "SR6: All Global Admin activations logged with justification, max 2 hours",
        "SR7: Leaked credential detections enabled with automated response",
    ],
    "technical": [
        "TR1: Risk-based CA policies use the modern approach -- not the legacy ID Protection portal",
        "TR2: The insider risk solution must use existing licences only",
        "TR3: Stale account automation requires no manual admin intervention after setup",
        "TR4: Named location config must not increase MFA friction for existing Auckland users",
        "TR5: Any new CA policies tested in report-only before enforcement",
        "TR6: Contractor identification uses a consistent attribute writable via PowerShell",
    ],
},

"CS3": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- cloud-only (no on-prem AD)"),
        ("Licence", "Entra ID P2 staff/academics | Entra ID Free for students"),
        ("External users", "1,240 B2B guest accounts -- researchers, sponsors, interns, academics"),
        ("Guest management", "No lifecycle policies -- created manually, never reviewed"),
        ("Access provisioning", "Manual IT ticket process -- average 8-day wait"),
        ("Entitlement Management", "Not configured -- no catalogs or access packages"),
        ("Access Reviews", "Not configured -- none ever run"),
        ("Connected organizations", "Not configured"),
        ("Cross-tenant sync", "Not configured"),
        ("Terms of Use", "Not configured -- no acceptance tracked"),
        ("SharePoint sharing", "Enabled with no restrictions -- any guest, any site"),
        ("Research systems", "ResearchHub, DataVault, GrantPortal, PublicationDB"),
    ],
    "business": [
        "BR1: External collaborators self-request access -- eliminate the IT ticket process",
        "BR2: 45 government researchers appear as seamless internal-looking users",
        "BR3: Corporate sponsor access auto-removed when their project ends",
        "BR4: Student intern guest accounts auto-disabled when placement ends",
        "BR5: Visiting academics accept a Data Handling ToU before accessing research systems",
        "BR6: Online students sign in with existing Google or Microsoft personal accounts",
    ],
    "security": [
        "SR1: All 1,240 existing guest accounts reviewed -- no active sponsor = removed",
        "SR2: Guest accounts cannot enumerate the full directory or see other guests",
        "SR3: SharePoint external sharing restricted to explicitly invited sites only",
        "SR4: DataVault access requires MFA regardless of home tenant MFA status",
        "SR5: No guest account has access beyond 12 months without an explicit renewal",
        "SR6: The 340 stale intern accounts disabled immediately",
    ],
    "technical": [
        "TR1: BR2 solution must not require individual B2B invitations for all 45 researchers",
        "TR2: Access packages used for all sponsor access -- not direct group assignment",
        "TR3: Solution uses existing P2 licences -- no additional purchase",
        "TR4: Online student sign-in uses External Identities -- not internal member accounts",
        "TR5: Terms of Use enforcement via Conditional Access -- not manual acknowledgement",
        "TR6: Access Reviews auto-remove access when reviewers do not respond",
    ],
},

"CS4": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- hybrid, Entra Connect Sync with PHS enabled"),
        ("Licence", "Microsoft Entra Suite for all staff (includes GSA, P2, Verified ID)"),
        ("Authentication", "Per-user MFA -- Authenticator push, no number matching"),
        ("Remote access", "Cisco AnyConnect VPN -- full tunnel, flat network access"),
        ("Network", "Single flat network -- no segmentation between application tiers"),
        ("Global Secure Access", "Licence available but NOT yet configured"),
        ("Shared devices", "240 field inspection staff on shared Windows 11 devices"),
        ("Internal apps", "GovPortal, CaseDB, RegDB, FieldApp"),
        ("M365 traffic", "All hairpinned through the VPN -- causing significant latency"),
        ("Conditional Access", "Require MFA (On), Block legacy auth (On) -- no GSA/risk conditions"),
        ("Certificate Authority", "On-premises PKI (AD CS) -- certificates issued to all devices"),
    ],
    "business": [
        "BR1: VPN decommissioned -- remote access uses Zero Trust, app-by-app not full network",
        "BR2: M365 traffic not hairpinned through the VPN or any on-prem proxy",
        "BR3: Field staff authenticate to FieldApp using certificates -- no smartphone",
        "BR4: 8 regional offices access GSA without installing the client on every device",
        "BR5: Remote workers cannot bypass GSA to access internal apps directly",
    ],
    "security": [
        "SR1: All staff use phishing-resistant MFA -- Authenticator push alone not acceptable",
        "SR2: CaseDB accessible only from compliant devices with phishing-resistant MFA",
        "SR3: The Private Network Connector requires no inbound firewall rules",
        "SR4: Any access to internal apps without going through GSA must be blocked",
        "SR5: MFA fatigue attacks must be prevented",
        "SR6: FieldApp access uses Certificate-Based Authentication configured as multi-factor",
    ],
    "technical": [
        "TR1: GSA deployment requires no additional licences -- use existing Entra Suite",
        "TR2: BR4 solution must not require the GSA client on individual branch devices",
        "TR3: M365 traffic optimisation uses the built-in GSA profile -- not custom config",
        "TR4: VPN remains operational in parallel -- decommission only after apps confirmed",
        "TR5: Certificate-based auth uses the existing on-premises PKI infrastructure",
        "TR6: All GSA traffic logged and visible in the GSA monitoring dashboard",
    ],
},

"CS5": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- cloud-only (no on-prem AD)"),
        ("Licence", "M365 F3 (frontline) / E3 (managers, corporate) + Entra ID P2 add-on"),
        ("Current groups", "847 groups total, mostly out of date -- all manually maintained"),
        ("Licence assignment", "Direct user assignment -- no group-based licensing"),
        ("SSPR", "Not enabled -- 340 weekly password resets go through helpdesk"),
        ("Lifecycle Workflows", "Not configured -- onboarding/offboarding are manual"),
        ("HR system", "Workday HR -- SCIM provisioning to Entra ID NOT yet configured"),
        ("Offboarding", "Manual -- manager emails IT, average 3-day delay to disable"),
        ("EuroStyle acquisition", "4,500 users in a separate tenant -- not yet migrated"),
        ("Seasonal workers", "Hired quarterly -- manual accounts, no automatic expiry"),
    ],
    "business": [
        "BR1: New store associates have day-one access with no IT ticket",
        "BR2: Department change auto-removes old access and assigns new access",
        "BR3: Seasonal workers automatically lose access exactly 13 weeks after start",
        "BR4: Password resets available to all staff via SSPR, no helpdesk needed",
        "BR5: EuroStyle staff migrated into the Northwind tenant within 60 days",
        "BR6: Licence assignment is automatic -- not manually assigned per user",
    ],
    "security": [
        "SR1: 3,400 former-employee accounts identified and disabled immediately",
        "SR2: Privilege creep prevented -- moving departments does not retain old access",
        "SR3: Seasonal worker accounts have a hard expiry, no manual renewal without IT",
        "SR4: Workday is the authoritative source for all identity lifecycle events",
        "SR5: All staff have 2+ SSPR methods registered before helpdesk stops accepting resets",
        "SR6: 1,200 stale licences detected and reclaimed",
    ],
    "technical": [
        "TR1: Group membership updates automatically when HR attributes change",
        "TR2: Solution uses the minimum number of dynamic groups necessary",
        "TR3: Workday provisions users via SCIM -- not CSV import or manual creation",
        "TR4: Lifecycle Workflows handle all joiner/mover/leaver scenarios automatically",
        "TR5: No additional licence purchases beyond existing F3/E3/P2",
        "TR6: EuroStyle migration uses cross-tenant user migration -- not manual recreation",
    ],
},

"CS6": {
    "environment": [
        ("Identity platform", "Hybrid -- on-prem AD (single forest, 3 domains) + Entra ID"),
        ("Entra Connect", "Running v2.1.x -- PHS configured but DISABLED, no writeback"),
        ("Authentication", "AD FS 2016 -- federated auth for all M365 and app sign-ins"),
        ("AD FS farm", "4 servers -- 3 unplanned outages in 18 months"),
        ("Legacy applications", "12 apps using AD FS as IdP -- 8 SAML 2.0, 4 WS-Federation"),
        ("Password Hash Sync", "Configured but DISABLED (domain is federated)"),
        ("ID Protection", "NOT available -- requires PHS or PTA"),
        ("Seamless SSO", "Not configured"),
        ("Domain status", "All 3 domains FEDERATED -- auth routed to AD FS"),
        ("Conditional Access", "Limited -- cannot evaluate sign-in risk without PHS/PTA"),
        ("Licence", "Entra ID P2 for all staff"),
    ],
    "business": [
        "BR1: No user disruption during migration -- authentication works throughout",
        "BR2: Migration allows rollback to AD FS at any point until apps confirmed",
        "BR3: Factory workers on domain-joined PCs get no MFA prompts on-site",
        "BR4: All 12 legacy apps migrated to Entra ID SSO before AD FS decommission",
        "BR5: AD FS farm decommissioned as the final step -- not before",
    ],
    "security": [
        "SR1: ID Protection (leaked credential detection, risk policies) enabled post-migration",
        "SR2: Password hashes synced to cloud -- PTA not acceptable, on-prem dependency risk",
        "SR3: Seamless SSO configured to eliminate auth prompts on the corporate network",
        "SR4: Legacy authentication blocked after migration completes",
        "SR5: AD FS application activity report used to assess migration readiness first",
    ],
    "technical": [
        "TR1: Cloud auth tested with a pilot group BEFORE converting domains from federated",
        "TR2: Entra Connect must NOT be installed on a domain controller",
        "TR3: Sequence: PHS -> Seamless SSO -> Staged Rollout pilot -> apps -> convert -> decommission",
        "TR4: Password writeback enabled before SSPR is deployed to users",
        "TR5: Solution enables ID Protection features not available with AD FS",
    ],
},

"CS7": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- cloud-only"),
        ("Licence", "Entra ID P2 + Workload Identities Premium for service principals"),
        ("App registrations", "234 total -- mix of internal apps, APIs, automation scripts"),
        ("Enterprise apps", "89 -- mix of gallery SaaS apps and custom apps"),
        ("Managed Identities", "Used for 28 Azure resources -- NOT for any app authentication"),
        ("Service accounts", "12 shared service accounts with passwords for app-to-app auth"),
        ("Hardcoded credentials", "67 apps with client secrets hardcoded in code or config"),
        ("API permissions", "34 apps have excessive permissions -- Global Reader when unneeded"),
        ("Admin consent", "8 apps have consented permissions that are never used"),
        ("SCIM provisioning", "Not configured for any SaaS app -- manual provisioning"),
        ("App Proxy", "Not configured -- 4 legacy on-prem apps not accessible remotely"),
    ],
    "business": [
        "BR1: All app-to-app authentication eliminates hardcoded credentials",
        "BR2: Salesforce provisioning fully automated -- manual process ends",
        "BR3: Remote staff access LegacyWarehouse without VPN, without app modification",
        "BR4: HR Sync App has the minimum permissions necessary for its function",
        "BR5: ReportingService client secret rotation is automated, not manual",
    ],
    "security": [
        "SR1: 12 service account passwords replaced with credential-free authentication",
        "SR2: 67 hardcoded client secrets replaced -- secrets never appear in source code",
        "SR3: All API permissions follow least privilege -- unused permissions removed",
        "SR4: CustomerPortal only accesses data for the currently signed-in customer",
        "SR5: Admin consent granted only for permissions actively used and documented",
        "SR6: Workload identity risk monitored -- anomalous service principal behaviour alerts",
    ],
    "technical": [
        "TR1: Azure-hosted workloads use Managed Identities -- not service accounts/secrets",
        "TR2: Secrets that can't use Managed Identity are stored in Azure Key Vault",
        "TR3: Salesforce provisioning uses SCIM 2.0 -- not a custom integration",
        "TR4: LegacyWarehouse published via Entra Application Proxy -- app not modified",
        "TR5: Minimum Graph API permission identified and applied for HR Sync App",
        "TR6: Workload identity risk monitoring requires the Workload Identities Premium licence",
    ],
},

"CS8": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- cloud-only"),
        ("Licence", "M365 E5 for all staff + M365 Copilot add-on for all staff"),
        ("Purview", "E5 Compliance included -- sensitivity labels NOT yet configured"),
        ("Copilot deployment", "Deployed to all staff -- NO governance controls configured"),
        ("Contractor access", "180 contractors as B2B guests -- currently have Copilot licence"),
        ("SharePoint permissions", "Widespread over-permissioning -- many stale inherited grants"),
        ("Sensitivity labels", "Not configured -- no data classification in place"),
        ("GSA", "Not deployed -- Entra Suite licence available but not configured"),
        ("Conditional Access", "Standard: MFA for all, block legacy auth"),
        ("Verified ID", "Licence available but not configured"),
        ("Shadow AI", "340 staff using personal ChatGPT -- no controls in place"),
        ("Audit logging", "Microsoft Purview audit logging enabled -- Copilot interactions logged"),
    ],
    "business": [
        "BR1: Copilot enabled for permanent staff only -- contractors must not have access",
        "BR2: Staff accept an AI Acceptable Use Policy before first Copilot use",
        "BR3: Copilot cannot surface or summarise strictly confidential content",
        "BR4: Shadow AI (personal ChatGPT etc.) blocked on corporate devices/networks",
        "BR5: Freelance talent verify identity digitally for contracts, no internal accounts",
        "BR6: All Copilot interactions auditable for compliance and investigation",
    ],
    "security": [
        "SR1: The over-permissioning root cause of Incident 1 must be addressed",
        "SR2: Strictly confidential documents protected regardless of user permissions",
        "SR3: Contractor B2B guests blocked from accessing Copilot entirely",
        "SR4: AI Acceptable Use Policy enforced via Conditional Access -- not self-service",
        "SR5: Unauthorised AI services blocked at the network level for all corporate traffic",
        "SR6: Copilot access logged including prompts submitted and content surfaced",
    ],
    "technical": [
        "TR1: Sensitivity labels use Microsoft Purview -- existing E5 licence includes this",
        "TR2: BR3/SR2 solution uses sensitivity labels to restrict Copilot -- not CA policies",
        "TR3: Shadow AI blocking uses GSA Internet Access -- not DNS blocking",
        "TR4: Contractor Copilot block uses CA policy targeting B2B guests -- not licence removal alone",
        "TR5: Verified ID solution does not require contractors/talent to create Microsoft accounts",
        "TR6: Copilot audit logs live in Microsoft Purview audit -- not Entra sign-in logs",
    ],
},

"CS9": {
    "environment": [
        ("Identity platform", "Microsoft Entra ID -- hybrid, Entra Connect with PHS"),
        ("Licence", "Entra ID P2 permanent staff | P1 contractors"),
        ("Access Reviews", "Never configured -- no reviews have ever been run"),
        ("Entitlement Management", "Partially configured -- 3 catalogs, no connected organizations"),
        ("External partner access", "340 partner users with direct group membership"),
        ("Identity Secure Score", "Currently 61/100 -- dropped from 74 in six months"),
        ("GSA", "Not deployed -- Entra Suite licence available"),
        ("Monitoring", "Diagnostic logs to Log Analytics -- no custom KQL alerts"),
        ("Clinical systems", "EMR, PharmacyDB, LabSystem, ImagingPACS -- audit trail required"),
        ("Secure Score drops", "MFA not required for admins, SSPR not enabled, stale accounts active"),
        ("Internet filtering", "No web content filtering -- clinical devices reach any site"),
    ],
    "business": [
        "BR1: 2,800 accounts with potentially inappropriate clinical access reviewed within 30 days",
        "BR2: External partner access uses self-service access packages -- not direct groups",
        "BR3: Specialist referral users request access themselves, auto-expires after 90 days",
        "BR4: Clinical devices cannot access social media, streaming, or personal cloud storage",
        "BR5: Identity Secure Score reaches 80+ within 90 days",
        "BR6: All access to EMR/clinical systems has a complete audit trail -- who approved, when",
    ],
    "security": [
        "SR1: Access reviews auto-remove access when reviewers don't respond within the period",
        "SR2: No external partner has standing access to clinical systems -- all time-limited",
        "SR3: Clinical device internet access filtered to block non-clinical websites",
        "SR4: KQL alerts for impossible travel, bulk export, and off-hours privileged activation",
        "SR5: Stale accounts (no sign-in 90+ days) automatically disabled",
        "SR6: MFA required for all administrator accounts",
    ],
    "technical": [
        "TR1: Access Reviews use the correct reviewer type -- self-review not acceptable for clinical",
        "TR2: Connected Organizations configured before external access packages can be requested",
        "TR3: GSA Internet Access used for clinical device web filtering -- not on-prem proxy",
        "TR4: KQL queries use SignInLogs for auth events, AuditLogs for directory changes",
        "TR5: Secure Score improvement actions implemented in the correct order",
        "TR6: The 2,800-account review completed before new access packages are deployed",
    ],
},

"CS10": {
    "environment": [
        ("Identity platform", "Hybrid -- 3 forests, Entra Connect with PHS"),
        ("Licence", "Entra Suite for permanent staff | Entra ID P1 for contractors"),
        ("TechVentures", "Separate tenant, 2,800 staff needing access to Meridian systems"),
        ("Authentication", "Authenticator push without number matching | SMS for contractors"),
        ("Privileged access", "8 permanent Global Admins | PIM only for Azure resources"),
        ("Remote access", "Cisco AnyConnect VPN -- three lateral-movement incidents"),
        ("Copilot", "Deployed to all staff including contractors -- no governance controls"),
        ("Azure workloads", "23 apps with hardcoded credentials -- Managed Identities unused"),
        ("Lifecycle", "Manual onboarding/offboarding -- former-employee incident occurred"),
        ("Entitlement Management", "Not configured -- all access via direct group assignment"),
        ("ID Protection", "Enabled -- no risk-based CA policies configured"),
        ("Secure Score", "54/100 -- multiple high-impact actions outstanding"),
    ],
    "business": [
        "BR1: TechVentures staff appear as internal users -- not external guests",
        "BR2: Employment end -> account disabled within 1 hour, automatically",
        "BR3: All contractors blocked from Copilot -- permanent staff may use it",
        "BR4: Remote workers access internal apps without VPN, using Zero Trust",
        "BR5: Privileged legal documents protected so Copilot cannot summarise them",
        "BR6: All Azure-hosted apps eliminate hardcoded credentials",
        "BR7: External client portal users sign in with their existing corporate identity",
    ],
    "security": [
        "SR1: MFA fatigue attacks prevented -- current Authenticator push is vulnerable",
        "SR2: All Global Admin access converted to PIM eligible -- max 2 permanent break-glass",
        "SR3: HIGH risk sign-ins automatically blocked via CA -- not manual review",
        "SR4: Contractor accounts must not use SMS OTP -- Authenticator minimum",
        "SR5: Personal cloud storage blocked at network level for all corporate devices",
        "SR6: All privileged role activations require justification, limited to 4 hours max",
        "SR7: The former-employee exfiltration incident cannot recur -- automated leaver controls",
    ],
    "technical": [
        "TR1: TechVentures integration requires no individual B2B invitations for 2,800 staff",
        "TR2: Leaver workflow triggers on employeeLeaveDateTime within 30 minutes of termination",
        "TR3: GSA Private Access replaces the VPN -- connector requires no inbound firewall rules",
        "TR4: Azure workloads use Managed Identities -- remaining secrets go to Key Vault",
        "TR5: Copilot content protection uses Purview sensitivity labels -- not CA policies",
        "TR6: Risk-based CA policies use the modern approach -- not the legacy ID Protection portal",
        "TR7: Personal cloud storage blocking uses GSA Internet Access -- not DNS",
    ],
},

}


def get_case_study_briefing(case_study_id: str):
    """Return the full Existing Environment + BR/SR/TR requirements for a
    case study -- the scenario scaffolding the questions reference by code
    (e.g. 'satisfies BR1 and TR3'). Returns None if not found."""
    cs_id = case_study_id.upper()
    if cs_id not in CASE_STUDY_REQUIREMENTS:
        return None
    return {"meta": CASE_STUDY_META[cs_id], "requirements": CASE_STUDY_REQUIREMENTS[cs_id]}


def display_case_study_briefing(case_study_id: str):
    """Print the full scenario briefing for a case study: company context,
    existing environment facts, and Business/Security/Technical
    Requirements -- everything the questions assume you've already read."""
    briefing = get_case_study_briefing(case_study_id)
    if not briefing:
        print(f"\n  [!]  No briefing found for '{case_study_id}'.\n")
        return
    meta = briefing["meta"]
    req = briefing["requirements"]
    separator = "=" * 70

    print(f"\n{separator}")
    print(f"  {case_study_id.upper()} -- {meta['title']}")
    print(separator)
    print(f"\n{meta['context']}\n")

    print("-- EXISTING ENVIRONMENT " + "-" * 45)
    for label, value in req["environment"]:
        print(f"  {label:<22} {value}")

    print("\n-- BUSINESS REQUIREMENTS " + "-" * 44)
    for item in req["business"]:
        print(f"  {item}")

    print("\n-- SECURITY REQUIREMENTS " + "-" * 44)
    for item in req["security"]:
        print(f"  {item}")

    print("\n-- TECHNICAL REQUIREMENTS " + "-" * 43)
    for item in req["technical"]:
        print(f"  {item}")

    print(f"\n{separator}\n")


# --------------------------------------------------------------------------
# GENERATOR / DISPLAY FUNCTIONS -- mirrors sc300_module.py conventions
# --------------------------------------------------------------------------

_REQ_CODE_PATTERN = re.compile(r"\b(BR|SR|TR)\d{1,2}\b")


def _lookup_requirement_line(cs_id: str, code: str):
    """Find the full requirement text for a code like 'BR1' within a given
    case study's business/security/technical requirement lists."""
    req = CASE_STUDY_REQUIREMENTS.get(cs_id)
    if not req:
        return None
    category = {"BR": "business", "SR": "security", "TR": "technical"}.get(code[:2])
    if not category:
        return None
    for line in req.get(category, []):
        if line.startswith(code + ":"):
            return line
    return None


def _extract_referenced_requirements(cs_id: str, text: str):
    """Scan question text for requirement codes (BR1, SR4, TR3, etc.) and
    return the full definition line for each one found, in first-seen
    order, deduplicated. Powers the 'what does SR1 actually say' need in
    single-question drill mode without printing the entire briefing."""
    seen = []
    for match in _REQ_CODE_PATTERN.finditer(text):
        code = match.group(0)
        if code not in seen:
            seen.append(code)
    lines = []
    for code in seen:
        line = _lookup_requirement_line(cs_id, code)
        if line:
            lines.append(line)
    return lines


def _format_pbq(q: dict) -> dict:
    meta = CASE_STUDY_META[q["case_study"]]
    return {
        "exam": f"{CASE_STUDY_EXAM['name']}",
        "id": q["id"],
        "case_study": f"{q['case_study']} -- {meta['title']}",
        "context": meta["context"],
        "domain": q["domain"],
        "difficulty": q["difficulty"],
        "question": q["question"],
        "options": q["options"],
        "correct": q["correct"],
        "explanation": q["explanation"],
        "pattern_refs": q.get("pattern_refs", []),
        "referenced_requirements": _extract_referenced_requirements(q["case_study"], q["question"]),
    }


def generate_case_study_pbq(case_study_filter=None, domain_filter=None, difficulty_filter=None):
    """Pick a random case study MCQ, optionally filtered by case study id,
    domain ('1'-'4', or the CS10 combined tags like '2+4'), or difficulty
    ('intermediate', 'advanced', 'final_boss')."""
    pool = CASE_STUDY_QUESTIONS
    if case_study_filter:
        pool = [q for q in pool if q["case_study"] == case_study_filter.upper()]
    if domain_filter:
        pool = [q for q in pool if domain_filter in q["domain"].split("+")]
    if difficulty_filter:
        filtered = [q for q in pool if q["difficulty"] == difficulty_filter]
        if filtered:
            pool = filtered
    if not pool:
        pool = CASE_STUDY_QUESTIONS
    return _format_pbq(random.choice(pool))


def generate_case_study_pbq_by_id(question_id: str):
    """Look up a specific question by ID (e.g. 'CS4-Q6'). Returns (pbq, err)
    -- mirrors sc300_search_patch.generate_sc300_pbq_by_id's (pbq, err) shape
    so start.py's Search-by-ID branch can call it the same way."""
    qid = question_id.strip().upper()
    for q in CASE_STUDY_QUESTIONS:
        if q["id"] == qid:
            return _format_pbq(q), None
    return None, f"No question found with ID '{question_id}'. Try e.g. CS4-Q6 or CS10-Q7."


def get_case_study_full_formatted(case_study_id: str):
    """Return (meta, [pbq, pbq, ...]) for all 8 questions in a case study,
    already formatted via _format_pbq -- ready to hand straight to
    display_case_study_pbq() in sequence for 'work through one case study' mode."""
    cs_id = case_study_id.upper()
    if cs_id not in CASE_STUDY_META:
        return None, []
    questions = [_format_pbq(q) for q in CASE_STUDY_QUESTIONS if q["case_study"] == cs_id]
    return CASE_STUDY_META[cs_id], questions


def show_case_study_scenario_index():
    """Print every question ID grouped by case study -- mirrors
    sc300_search_patch.show_sc300_scenario_index() for the '?' menu option."""
    print("\nSC-300 Case Study Question Index\n" + "=" * 40)
    for cs_id, meta in CASE_STUDY_META.items():
        print(f"\n{cs_id} -- {meta['title']}")
        for q in CASE_STUDY_QUESTIONS:
            if q["case_study"] == cs_id:
                print(f"   {q['id']}  [Domain {q['domain']}]  {q['question'][:70]}...")
    print()


def get_weighted_case_study_pbq():
    """Weighted by SC-300 domain exam weighting, same weights as sc300_module."""
    weights = [22, 28, 22, 28]
    domain = random.choices(["1", "2", "3", "4"], weights=weights, k=1)[0]
    return generate_case_study_pbq(domain_filter=domain)


def get_final_boss_pbq():
    """Surface a CS10 multi-domain question specifically."""
    return generate_case_study_pbq(case_study_filter="CS10")


def get_case_study_full(case_study_id: str):
    """Return metadata + all 8 questions for a specific case study (for
    'Case Study Mode' -- work through one full case study in order)."""
    cs_id = case_study_id.upper()
    if cs_id not in CASE_STUDY_META:
        return None
    questions = [q for q in CASE_STUDY_QUESTIONS if q["case_study"] == cs_id]
    return {"meta": CASE_STUDY_META[cs_id], "questions": questions}


def search_pattern_library(keyword: str):
    """Case-insensitive search across the pattern library text."""
    keyword = keyword.lower()
    return [p for p in PATTERN_LIBRARY if keyword in p["pattern"].lower()]


def get_patterns_by_domain(domain: str):
    return [p for p in PATTERN_LIBRARY if p["domain"] == domain]


def display_case_study_pbq(pbq: dict, student_mode: bool = False):
    separator = "=" * 70
    print(f"\n{separator}")
    print(f"  {pbq.get('exam', 'SC-300 Case Studies')}")
    print(f"  Case Study  : {pbq.get('case_study', 'N/A')}")
    print(f"  Question ID : {pbq.get('id', 'N/A')}")
    print(f"  Domain      : {pbq.get('domain', 'N/A')}")
    print(f"  Difficulty  : {pbq.get('difficulty', 'N/A').upper()}")
    print(separator)
    print(f"\nContext: {pbq.get('context', '')}\n")
    refs_needed = pbq.get("referenced_requirements", [])
    if refs_needed:
        print("Requirements referenced in this question:  (BR = Business, SR = Security, TR = Technical)")
        for line in refs_needed:
            print(f"  - {line}")
        print()
    print(pbq.get("question", "No question generated."))
    for letter, text in pbq.get("options", {}).items():
        print(f"  {letter}. {text}")
    if not student_mode:
        print(f"\n{separator}")
        print(f"  CORRECT ANSWER: {pbq.get('correct', '?')}")
        print(separator)
        print(pbq.get("explanation", ""))
        refs = pbq.get("pattern_refs", [])
        if refs:
            print(f"\n  Pattern(s): {'; '.join(refs)}")
    print(f"\n{separator}\n")


def display_case_study_index():
    """Print the 10 case studies with company, focus, and domain coverage --
    used for a 'Case Study Mode' menu listing."""
    print("\nSC-300 Case Study Library -- 10 case studies, 80 questions\n")
    for cs_id, meta in CASE_STUDY_META.items():
        print(f"{cs_id}: {meta['title']}")
        print(f"   Focus: {meta['focus']}")
        print(f"   Domains: {', '.join(meta['domains'])}\n")


if __name__ == "__main__":
    print("\nGIDEON - SC-300 Case Study Module Test")
    print("Generating 3 sample case study questions (weighted by domain)...\n")
    for i in range(3):
        pbq = get_weighted_case_study_pbq()
        display_case_study_pbq(pbq, student_mode=False)
        input("Press ENTER for next question...\n")
    print("\nAnd one Final Boss (CS10) question:\n")
    display_case_study_pbq(get_final_boss_pbq(), student_mode=False)