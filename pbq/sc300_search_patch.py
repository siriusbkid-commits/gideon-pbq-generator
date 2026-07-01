"""
SC-300 Scenario ID lookup — add these functions to sc300_module.py
and wire into gideon.py menu (see instructions at bottom).
"""
import random

# ── Scenario ID index ────────────────────────────────────────────────────────

SC300_SCENARIO_INDEX = {
    # Domain 1
    "SC1-001": ("1", 0),
    "SC1-002": ("1", 1),
    "SC1-003": ("1", 2),
    "SC1-004": ("1", 3),
    # Domain 2
    "SC2-001": ("2", 0),
    "SC2-002": ("2", 1),
    "SC2-003": ("2", 2),
    "SC2-004": ("2", 3),
    # Domain 3
    "SC3-001": ("3", 0),
    "SC3-002": ("3", 1),
    "SC3-003": ("3", 2),
    # Domain 4
    "SC4-001": ("4", 0),
    "SC4-002": ("4", 1),
    "SC4-003": ("4", 2),
    "SC4-004": ("4", 3),
}

SC300_SCENARIO_TOPICS = {
    "SC1-001": "Tenant config, admin roles, company branding, guest settings",
    "SC1-002": "Bulk user creation, dynamic groups, licensing, custom attributes",
    "SC1-003": "Hybrid identity, Entra Connect, PHS vs PTA vs AD FS, Seamless SSO",
    "SC1-004": "External identities, B2B, Google federation, cross-tenant access",
    "SC2-001": "Conditional Access design, report-only, auth context, What If tool",
    "SC2-002": "MFA methods, SSPR, WHfB, FIDO2, per-user MFA migration",
    "SC2-003": "ID Protection, user/sign-in risk, risk policies, impossible travel",
    "SC2-004": "Global Secure Access, Private Access vs Internet Access, ZTNA",
    "SC3-001": "Managed identities, service principals, AKS WIF, Key Vault, RBAC",
    "SC3-002": "Enterprise app SSO, SAML/OIDC, SCIM provisioning, App Proxy",
    "SC3-003": "App registrations, OAuth 2.0 flows, API permissions, certificates",
    "SC4-001": "PIM, eligible vs active, break-glass, PIM for Groups, Azure resources",
    "SC4-002": "Access Reviews, no-response settings, Lifecycle Workflows, offboarding",
    "SC4-003": "Entitlement Management, access packages, catalogs, Terms of Use",
    "SC4-004": "Monitoring, KQL, Workbooks, Diagnostic Settings, Secure Score",
}


def generate_sc300_pbq_by_id(scenario_id: str, student_mode: bool = False):
    """
    Generate a randomised SC-300 PBQ for a specific scenario ID.
    Variables are still randomised — the template is fixed.
    """
    sid = scenario_id.upper().strip()

    if sid not in SC300_SCENARIO_INDEX:
        return None, f"Unknown scenario ID '{sid}'. Valid IDs: {', '.join(sorted(SC300_SCENARIO_INDEX.keys()))}"

    domain, idx = SC300_SCENARIO_INDEX[sid]

    from pbq.sc300_module import (
        DOMAIN1_SCENARIOS,
        DOMAIN2_SCENARIOS,
        DOMAIN3_SCENARIOS,
        DOMAIN4_SCENARIOS,
        SC300_EXAM,
        display_sc300_pbq,
    )

    domain_map = {
        "1": DOMAIN1_SCENARIOS,
        "2": DOMAIN2_SCENARIOS,
        "3": DOMAIN3_SCENARIOS,
        "4": DOMAIN4_SCENARIOS,
    }

    template = domain_map[domain][idx]
    scenario_text = template["scenario_template"]

    for var_name, options in template.get("variables", {}).items():
        chosen = random.choice(options)
        scenario_text = scenario_text.replace(f"{{{var_name}}}", chosen)

    domain_info = SC300_EXAM["domains"][domain]

    pbq = {
        "exam":            f"{SC300_EXAM['name']} ({SC300_EXAM['code']})",
        "id":              template["id"],
        "domain":          f"{domain}. {domain_info['name']} ({domain_info['weight']}%)",
        "sub_topic":       template["sub_topic"],
        "objective":       template["objective"],
        "difficulty":      template["difficulty"],
        "exam_objectives": ", ".join(template.get("exam_objectives", [])),
        "scenario":        scenario_text.strip(),
        "answers":         template.get("answers", "No answers available."),
        "targeted":        True,
    }

    return pbq, None


def display_sc300_pbq_with_nudge(pbq: dict, student_mode: bool = False):
    """
    Extended display that adds the exam-readiness nudge when a specific
    scenario ID was requested (pbq['targeted'] == True).
    """
    from pbq.sc300_module import display_sc300_pbq
    display_sc300_pbq(pbq, student_mode=student_mode)

    if pbq.get("targeted"):
        print("  💡 For exam readiness, also try Random Mode — the real exam")
        print("     won't tell you which domain is coming. Mix targeted drills")
        print("     with random sessions to build full exam confidence.\n")


def show_sc300_scenario_index():
    """Print the full scenario ID index — useful as a help screen."""
    print("\n" + "=" * 65)
    print("  SC-300 SCENARIO ID QUICK REFERENCE")
    print("=" * 65)
    domains_display = {
        "1": "Domain 1 — Implement and Manage User Identities (20-25%)",
        "2": "Domain 2 — Authentication and Access Management (25-30%)",
        "3": "Domain 3 — Plan and Implement Workload Identities (20-25%)",
        "4": "Domain 4 — Plan and Automate Identity Governance (25-30%)",
    }
    current_domain = None
    for sid in sorted(SC300_SCENARIO_INDEX.keys()):
        domain = SC300_SCENARIO_INDEX[sid][0]
        if domain != current_domain:
            current_domain = domain
            print(f"\n  {domains_display[domain]}")
            print(f"  {'-' * 60}")
        topic = SC300_SCENARIO_TOPICS.get(sid, "")
        print(f"  {sid}  —  {topic}")
    print("\n" + "=" * 65 + "\n")